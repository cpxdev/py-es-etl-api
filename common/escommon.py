from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch(host='localhost', port=9200)
es = Elasticsearch()
