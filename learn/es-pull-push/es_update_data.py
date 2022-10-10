# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from const import (
    ES_HOST,
    ES_PORT
)

es = Elasticsearch(host=ES_HOST, port=ES_PORT)
es = Elasticsearch()


# update by index
def update_data_by_index(_index, _doc_type, _id, update_data):
    res = es.update(
        index=_index,
        doc_type=_doc_type,
        id=_id,
        body=update_data
    )
    return res


# update by query
def update_by_query(_index, query, field, update_data):
    _inline = "ctx._source.{field}={update_data}".format(
        field=field, update_data=update_data)
    _query = {
        "script": {
            "inline": _inline,
        },
        "query": {
            "match": query
        }
    }
    res = es.update_by_query(body=_query, index=_index)
    return res


# update by bulk api
def update_by_bulk(_index, _id, update_data, doc_type):
    action = [{
        "_id": _id,
        "_type": doc_type,
        "_index": _index,
        "_source": {"doc": update_data},
        "_op_type": 'update'
    }]
    res = helpers.bulk(es, action)
    return res


if __name__ == "__main__":
    index = "test-index"
    _id = 5
    _doc_type = "authors"
    update_data = {
        "doc": {"age": 26}
    }
    res = update_data_by_index(index, _doc_type, _id, update_data)
    query = {"author": "Chestermo"}
    field = "age"
    update_data = 50
    res = update_by_query(index, query, field, update_data)
    update_data = {"age": 27}
    res = update_by_bulk(index, _id, update_data, _doc_type)
