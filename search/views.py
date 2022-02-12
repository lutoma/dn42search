from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from searchdb.models import URL
import pysolr

solr = pysolr.Solr('http://localhost:8983/solr/dn42search', always_commit=True)


class IndexView(TemplateView):
	template_name = 'index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		solr_result = solr.search('*:*', rows=0)
		context['index_size'] = solr_result.hits
		return context

# http://localhost:8983/solr/dn42search/query?q=*:*&rows=0


class SearchResultsView(TemplateView):
	template_name = 'search_results.html'

	def get(self, *args, **kwargs):
		self.query = self.request.GET.get('q')
		if not self.query:
			return HttpResponseRedirect('/')

		return super().get(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['query'] = self.query

		try:
			solr_result = solr.search(self.query)
		except pysolr.SolrError as e:
			context['error'] = e
			return context

		context['results'] = solr_result.docs
		context['results_count'] = solr_result.hits
		return context
