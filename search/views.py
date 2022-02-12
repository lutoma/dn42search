from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from searchdb.models import URL
import pysolr
import requests

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

		http_response = requests.get('http://localhost:8983/solr/dn42search/select', params={
			'q': self.query,
			'fl': 'id,title,excerpt,url,size,last_indexed,mime'
		})

		data = http_response.json()

		if 'error' in data:
			context['error'] = data['error']['msg']
			return context

		response = data['response']

		context['results'] = response['docs']
		context['results_count'] = response['numFound']
		return context
