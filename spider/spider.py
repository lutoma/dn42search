import requests
from requests_toolbelt.adapters.source import SourceAddressAdapter
from requests_toolbelt.cookies.forgetful import ForgetfulCookieJar
from urllib.parse import urljoin, urlparse, urlunparse
from django.utils import timezone
import robots
import pysolr

from searchdb.models import Host
from .parsers import MIME_PARSERS

import urllib3
import socket
urllib3.disable_warnings()
socket.setdefaulttimeout(3.05)

solr = pysolr.Solr('http://localhost:8983/solr/dn42search', always_commit=True)

BLACKLIST_DOMAINS = {
	'ca.dn42',
	'wiki.burble.dn42',
	'internal.dn42',
	'files.nop.dn42' # tmp
}

# These would get rejected during the crawl anyway due to the mime type/
# content-length. But if we can reject them in the add stage we save a HEAD
# request and avoid putting unnecessary load on servers.
BLACKLIST_EXTENSIONS = {
	'exe', 'zip', 'tar', 'gz', 'bin', 'vmdk', 'ova', 'iso', 'tgz', 'mp3',
	'ogg', 'flac', 'opus', 'wav', '7z', 'img', 'lyric', 'rar', 'pdf', 'jpg',
	'png', 'gif', 'tif', 'tiff', 'arj', 'mov', 'bmp', 'ape'
}


class CrawlTarget:
	url = None
	up = None

	def __init__(self, url, up):
		self.url = url
		self.up = up

	def __str__(self):
		return self.url

	def __eq__(self, other):
		if other == self.url:
			return True
		return False

	def __hash__(self):
		return hash(self.url)


class Crawler:
	queue = set()
	crawled = set()
	robots_txt_map = dict()

	def __init__(self):
		self.session = requests.Session()
		self.session.verify = False
		self.session.mount('http://', SourceAddressAdapter('172.23.13.14'))
		self.session.mount('https://', SourceAddressAdapter('172.23.13.14'))

		self.session.cookies = ForgetfulCookieJar()
		self.session.headers.update({
			'User-Agent': 'dn42search spider (+https://search.dn42)',
			'Accept-Encoding': None
		})

	def queue_url(self, url):
		up = urlparse(url)

		# Ignore fragments (https://example.org/foo#bar <- the bar part)
		up = up._replace(fragment=None)
		url = up.geturl()

		if url in self.crawled or url in self.queue:
			return

		if up.scheme not in {'http', 'https'}:
			return

		if up.hostname in BLACKLIST_DOMAINS:
			return

		# FIXME Maybe add support for DN42 ip addresses later
		tld = up.hostname.rsplit('.', maxsplit=1)[-1]
		if tld != 'dn42':
			return

		# Fast and loose filtering of extensions to save HEAD requests
		filename_split = up.path.split('/')[-1].split('.')
		if len(filename_split) > 1 and filename_split[-1].lower() in BLACKLIST_EXTENSIONS:
			return

		print(f'  -> New URL queued: {url}')
		target = CrawlTarget(url, up)
		self.queue.add(target)

	def crawl(self):
		while self.queue:
			self.crawl_url(self.queue.pop())

	def fetch_url(self, url, method='get', *args, **kwargs):
		try:
			response = getattr(self.session, method)(url, allow_redirects=False,
				timeout=(3.05, 10), *args, **kwargs)
			response.raise_for_status()
			return response
		except requests.exceptions.RequestException:
			return None

	def get_robots_txt(self, target):
		robots_txt_url = urlunparse((target.up.scheme, target.up.netloc, 'robots.txt', None, None, None))

		if robots_txt_url in self.robots_txt_map:
			return self.robots_txt_map[robots_txt_url]

		print(f'No cache for {robots_txt_url}, fetching')

		response = self.fetch_url(robots_txt_url)
		if not response or response.status_code != 200:
			self.robots_txt_map[robots_txt_url] = None
			return None

		rp = robots.RobotsParser.from_string(response.text)
		self.robots_txt_map[robots_txt_url] = rp
		return rp

	def crawl_url(self, target):
		print(f'Crawling {target}')

		robotstxt = self.get_robots_txt(target)
		if robotstxt and not robotstxt.can_fetch('dn42search', target.url):
			print('  Denied by robots.txt')
			return

		response = self.fetch_url(target.url, method='head')
		self.crawled.add(target.url)

		if not response:
			print('  No response to HEAD request')
			return

		# FIXME response error handling
		# FIXME Check status code
		if 'location' in response.headers:
			dest = urljoin(target.url, response.headers['location'])
			self.queue_url(dest)
			print('  Redirect')
			return

		try:
			length = int(response.headers['content-length'])
		except (KeyError, ValueError):
			print('  No or invalid content-length')
			return

		if length > 5242880:
			print('  content-length > 5 MiB, bailing')
			return

		if 'content-type' not in response.headers:
			print('  No content type')
			return

		# Transform things like `text/html; charset=utf-8` into just `text/html`
		effective_content_type = response.headers['content-type'].split(';')[0]
		if effective_content_type not in MIME_PARSERS:
			# FIXME Unsupported types should still be added to URL database, just not parsed/requested
			print(f'  Unsupported content type `{effective_content_type}`')
			return

		# Now that we have checked the headers, load the file for real
		response = self.fetch_url(target.url, stream=True)
		if not response:
			print('  No response to GET request')
			return

		parser = MIME_PARSERS[effective_content_type]()
		if not parser.parse(response.text):
			return

		for link in parser.get_links():
			dest = urljoin(target.url, link)
			self.queue_url(dest)

		try:
			host = Host.objects.get_or_create(name=target.up.hostname,
				defaults={'last_crawl': timezone.now()})[0]

			response.raw.decode_content = True
			text = parser.get_text()
			title = parser.get_title()
			excerpt = parser.get_excerpt()

			url, _ = host.urls.update_or_create(url=target.url, defaults={
				'last_crawl': timezone.now(),
				'headers': dict(response.headers),
				'title': title,
				'excerpt': excerpt,
				'text': text,
				'content': response.raw.read()
			})
		except Exception as e:
			print('  Could not store result', e)
			return

		solr.add([{
			'id': url.id,
			'title': title,
			'excerpt': excerpt,
			'text': text,
			'url': target.url
		}])
