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
def read_search(q: str, page: Optional[int] = 1, fields: Optional[str] = 'url,title,excerpt'):
		http_response = requests.get('http://localhost:8983/solr/dn42search/select', params={
			'defType': 'edismax',
			'q': q,
			'fl': fields,
			'qf': 'hostname^8 url^3 title^5 excerpt^4 text^3 mime^0.5',
			'rows': 15,
			'start': (page - 1) * 15,
			'mm': '50%',
		})

		data = http_response.json()

		if 'error' in data:
			return {'status': 'error', 'error': data['error']['msg']}

		response = data['response']
		return {
			'status': 'ok',
			'count': response['numFound'],
			'pages': ceil(response['numFound'] / 15),
			'results': response['docs']
		}
