from bs4 import BeautifulSoup
from boilerpy3 import extractors
from textwrap import shorten

canola_extractor = extractors.CanolaExtractor()
article_extractor = extractors.ArticleExtractor()


class BaseParser:
	links = set()
	text = None
	title = None
	excerpt = None

	def parse(self, data):
		pass

	def get_links(self):
		return self.links

	def get_text(self):
		return self.text

	def get_title(self):
		return self.title

	def get_excerpt(self):
		return shorten(self.get_text().replace('\n', ' '), width=300, placeholder='…')


class HTMLParser(BaseParser):
	data = None
	soup = None
	robots_meta = set()

	def parse(self, data):
		self.data = data
		self.soup = BeautifulSoup(data, 'html.parser')

		robots_meta_attr = self.soup.find('meta', attrs={'name': 'robots'})
		if robots_meta_attr:
			self.robots_meta = robots_meta_attr['content'].split(',')

		if 'noindex' in self.robots_meta:
			print('  robots meta tag contains `noindex`, bailing.')
			return False

		if self.soup.title:
			self.title = self.soup.title.string

		return True

	def get_links(self):
		if 'nofollow' in self.robots_meta:
			print('  robots meta tag contains `nofollow`, not parsing links.')
			return set()

		links = set()
		for link in self.soup.find_all('a'):
			if 'rel' in link:
				if 'nofollow' in link['rel'].split(','):
					continue

			links.add(link.get('href'))

		return links

	def get_text(self):
		blacklist = {'[document]', 'noscript', 'header', 'html', 'meta', 'head',
			'input', 'script', 'body', 'style'}

		output = list()
		for t in self.soup.find_all(text=True):
			if t.parent.name not in blacklist:
				output.append(t)

		return ' '.join(output)

	def get_excerpt(self):
		for tag in ['description', 'og:description']:
			desc_attr = self.soup.find('meta', attrs={'name': tag})
			if desc_attr:
				return desc_attr['content'][:500]

		try:
			text = canola_extractor.get_content(self.data)

			if len(text) < 150:
				# Retry with article extractor
				text_article = article_extractor.get_content(self.data)
				text = max(text, text_article, key=len)
		except Exception:
			return ''

		return shorten(text, width=300, placeholder='…')


class TextParser(BaseParser):
	def parse(self, data):
		self.data = data
		return True

	def get_text(self):
		return self.data


MIME_PARSERS = {
	'text/html': HTMLParser,
	'text/plain': TextParser
}
