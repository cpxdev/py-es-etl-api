# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from const import (
    ES_HOST,
    ES_PORT
)

es = Elasticsearch(host=ES_HOST, port=ES_PORT)
es = Elasticsearch()


def delete_data_by_bulk(_index, _doc_type, _id):
    action = [
        {
            '_op_type': 'delete',
            '_index': _index,
            '_type': _doc_type,
            '_id': _id,
        }
    ]
    res = helpers.bulk(es, action)
    return res


# clear all index items
def delete_index(_index):
    res = es.indices.delete(index=_index, ignore=[400, 404])
    return res


# delete content but empty item exist
def delete_by_query(_index, query):
    res = es.delete_by_query(
        index=_index,
        body={"query": {"match": query}}
    )
    return res


# delet all item
def delete_one(_index, _id):
    res = es.delete(index=_index, id=_id)
    return res


if __name__ == "__main__":
    _index = "test-index"
    query = {"author": "Ken"}
    res = delete_by_query(_index, query)
    _id = "1"
    res = delete_one(_index, _id)
