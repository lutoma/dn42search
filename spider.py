import requests
from requests_toolbelt.adapters.source import SourceAddressAdapter
from requests_toolbelt.cookies.forgetful import ForgetfulCookieJar
from urllib.parse import urljoin, urlparse, urlunparse
from time import sleep, time
import robots
import pysolr
import redis
import yaml
from sdnotify import SystemdNotifier

from parsers import MIME_PARSERS

import urllib3
import socket
urllib3.disable_warnings()
socket.setdefaulttimeout(3.05)


class Crawler:
	robots_txt_map = dict()

	def __init__(self):
		with open('config.yml') as fp:
			self.config = yaml.safe_load(fp)

		self.sdnotify = SystemdNotifier()

		self.solr = pysolr.Solr(self.config['solr_endpoint'], always_commit=True)
		self.redis = redis.Redis(
			host=self.config.get('redis_host', 'localhost'),
			port=self.config.get('redis_port', 6379),
			db=self.config.get('redis_db', 0))

		self.session = requests.Session()
		self.session.verify = False

		source_ip = self.config.get('crawl_source_ip', '0.0.0.0')
		self.session.mount('http://', SourceAddressAdapter(source_ip))
		self.session.mount('https://', SourceAddressAdapter(source_ip))

		self.session.cookies = ForgetfulCookieJar()
		self.session.headers.update({
			'User-Agent': self.config['user_agent'],
			'Accept-Encoding': None
		})

	def queue_url(self, url):
		up = urlparse(url)

		# Ignore fragments (https://example.org/foo#bar <- the bar part)
		up = up._replace(fragment=None)
		url = up.geturl()

		if self.redis.sismember('queue', url) or self.redis.zscore('known', url):
			return

		if up.scheme not in {'http', 'https'}:
			return

		if up.hostname in self.config.get('blacklist_domains', []):
			return

		# FIXME Maybe add support for DN42 ip addresses later
		tld = up.hostname.rsplit('.', maxsplit=1)[-1]
		if tld != 'dn42':
			return

		print(f'  -> New URL queued: {url}')
		self.redis.sadd('queue', url)

	def fetch_url(self, url, method='get', *args, **kwargs):
		try:
			response = getattr(self.session, method)(url, allow_redirects=False,
				timeout=(3.05, 10), *args, **kwargs)
			response.raise_for_status()
			return response
		except Exception:
			return None

	def get_robots_txt(self, up):
		robots_txt_url = urlunparse((up.scheme, up.netloc, 'robots.txt', None, None, None))

		# Check primary object cache
		# It migth be worth caching the text response in redis later on if we
		# end up restarting the crawling process frequently or if there will be
		# multiple concurrent ones
		if robots_txt_url in self.robots_txt_map:
			return self.robots_txt_map[robots_txt_url]

		print(f'  No cache for {robots_txt_url}, fetching')

		response = self.fetch_url(robots_txt_url)
		if not response or response.status_code != 200:
			self.robots_txt_map[robots_txt_url] = None
			return None

		rp = robots.RobotsParser.from_string(response.text)
		self.robots_txt_map[robots_txt_url] = rp
		return rp

	def crawl_url(self, url):
		up = urlparse(url)

		# Check again in case host was added to blacklist after URL was already queued
		if up.hostname in self.config.get('blacklist_domains', []):
			return

		print(f'Crawling {url}')

		robotstxt = self.get_robots_txt(up)
		if robotstxt and not robotstxt.can_fetch('dn42search', url):
			print('  Denied by robots.txt')
			return

		response = self.fetch_url(url, method='head')
		self.redis.zadd('known', {url: int(time())})

		if not response:
			print('  No response to HEAD request')
			return

		# FIXME response error handling
		# FIXME Check status code
		if 'location' in response.headers:
			dest = urljoin(url, response.headers['location'])
			self.queue_url(dest)
			print(f'  Redirect to {dest}')
			return

		skip_download = False

		try:
			size = int(response.headers['content-length'])
			if size > self.config.get('max_response_size', 5242880):
				print('  content-length too large')
				skip_download = True
		except (KeyError, ValueError):
			print('  No or invalid content-length')
			skip_download = True
			size = None

		if 'content-type' not in response.headers:
			print('  No content type')
			skip_download = True
			effective_content_type = None
		else:
			# Transform things like `text/html; charset=utf-8` into just `text/html`
			effective_content_type = response.headers['content-type'].split(';')[0]
			if effective_content_type not in MIME_PARSERS:
				skip_download = True

		data = {
			'id': url,
			'url': url,
			'mime': effective_content_type,
			'size': size,
			'server': response.headers.get('server'),

			# Will be updated below if a better title is found
			'title': url.rsplit('/', maxsplit=1)[-1]
		}

		if not skip_download:
			# Now that we have checked the headers, load the file for real
			response = self.fetch_url(url, stream=True)
			if not response:
				print('  No response to GET request')
				return

			parser = MIME_PARSERS[effective_content_type]()
			if not parser.parse(response.text):
				return

			absolute_links = []
			for link in parser.get_links():
				dest = urljoin(url, link)
				absolute_links.append(dest)
				self.queue_url(dest)

			new_data = {
				'title': parser.get_title(),
				'excerpt': parser.get_excerpt(),
				'text': parser.get_text(),
				'links': absolute_links,
			}

			data.update((k, v) for k, v in new_data.items() if v is not None)

		self.solr.add([data])

	def run(self):
		self.sdnotify.notify("READY=1")

		while True:
			# Check for old known URLs that are due for re-crawling
			ts = int(time()) - self.config.get('recrawl_after', 86400)
			recrawl = self.redis.zrange('known', 0, ts, byscore=True)
			if recrawl:
				print('Due for recrawling:', recrawl)
				self.redis.sadd('queue', *recrawl)
				self.redis.zremrangebyscore('known', 0, ts)

			# Retrieve URL to crawl
			target = self.redis.spop('queue')
			if not target:
				sleep(5)
				continue

			target = target.decode('utf-8')
			self.crawl_url(target)


if __name__ == '__main__':
	import sys
	c = Crawler()

	if len(sys.argv) > 1:
		c.queue_url(sys.argv[1])

	c.run()
