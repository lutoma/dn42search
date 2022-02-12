from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import HStoreField
from django.db import models


class Host(models.Model):
	name = models.CharField(max_length=255, verbose_name=_('Hostname'), unique=True)
	last_crawl = models.DateTimeField(verbose_name=_('Last crawl time'))

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']


class URL(models.Model):
	host = models.ForeignKey(Host, on_delete=models.CASCADE,
		related_name='urls', verbose_name=_('Hostname'))

	url = models.CharField(max_length=2048, verbose_name=_('URL'), unique=True)
	last_crawl = models.DateTimeField(verbose_name=_('Last crawl time'))

	headers = HStoreField(verbose_name=_('Response headers'), null=True)
	title = models.CharField(max_length=2048, verbose_name=_('Title'), blank=True, null=True)
	excerpt = models.CharField(max_length=1024, verbose_name=_('Excerpt'), blank=True, null=True)
	text = models.TextField(verbose_name=_('Extracted text'), blank=True, null=True)

	content = models.BinaryField(verbose_name=_('Content'), blank=True)

	def __str__(self):
		return self.url

	class Meta:
		ordering = ['url']
