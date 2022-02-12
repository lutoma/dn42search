from django.core.management.base import BaseCommand
from ...spider import Crawler


class Command(BaseCommand):
	help = 'Manually runs spider against selected host'

	def add_arguments(self, parser):
		parser.add_argument('url', type=str, help='URL to crawl')

	def handle(self, *args, **kwargs):
		c = Crawler()
		c.queue_url(kwargs['url'])
		c.crawl()
