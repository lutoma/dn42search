from fastapi import FastAPI
import requests

app = FastAPI()


@app.get("/")
def read_root():
	http_response = requests.get('http://search.dn42:8983/solr/dn42search/select', params={
		'q': '*:*',
		'fl': '',
		'rows': 0
	})
	data = http_response.json()
	return {'status': 'ok', 'index_size': data['response']['numFound']}


@app.get("/search/")
def read_item(q: str):
		http_response = requests.get('http://search.dn42:8983/solr/dn42search/select', params={
			'q': q,
			'fl': 'id,title,excerpt,url,size,last_indexed,mime'
		})

		data = http_response.json()

		if 'error' in data:
			return {'status': 'error', 'error': data['error']['msg']}

		response = data['response']
		return {'status': 'ok', 'count': response['numFound'], 'results': response['docs']}
