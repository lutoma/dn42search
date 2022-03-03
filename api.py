from fastapi import FastAPI
from typing import Optional
from math import ceil
import requests

app = FastAPI()


@app.get("/")
def read_root():
	http_response = requests.get('http://localhost:8983/solr/dn42search/select', params={
		'q': '*:*',
		'fl': '',
		'rows': 0
	})
	data = http_response.json()
	return {'status': 'ok', 'index_size': data['response']['numFound']}


@app.get("/search")
def read_search(q: str, page: Optional[int] = 1,
	fields: Optional[str] = 'url,title,excerpt,domain', group_domains: Optional[bool] = True):

	params = {
		'defType': 'edismax',
		'q': q,
		'fl': fields,
		'qf': 'hostname^8 url^3 title^5 excerpt^4 text^3 mime^0.5',
		'rows': 15,
		'start': (page - 1) * 15,
		'mm': '50%'
	}

	if group_domains:
		params.update({
			'fq': '{!collapse field=domain}',
			'expand': 'true'
		})

	http_response = requests.get('http://localhost:8983/solr/dn42search/select', params=params)

	data = http_response.json()

	if 'error' in data:
		return {'status': 'error', 'error': data['error']['msg']}

	solr_response = data['response']
	response = {
		'status': 'ok',
		'count': solr_response['numFound'],
		'pages': ceil(solr_response['numFound'] / 15),
		'results': solr_response['docs'],
	}

	if 'expanded' in data:
		response['more'] = data['expanded']

	return response
