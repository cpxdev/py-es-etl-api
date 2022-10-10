# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
from const import (
    ES_HOST,
    ES_PORT
)

es = Elasticsearch(host=ES_HOST, port=ES_PORT)
es = Elasticsearch()


def search_by_index_and_id(_index, _id):
    res = es.get(
        index=_index,
        id=_id
    )
    return res


def search_by_index_and_query(_index, _doc_type, query):
    res = es.search(
        index=_index,
        body=query
    )
    return query


if __name__ == "__main__":
    index = "test-index"
    _id = 5
    res = search_by_index_and_id(index, _id)
    _doc_type = "authors"
    query = {}
    search_by_index_and_query(index, _doc_type, query)
