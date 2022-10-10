# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
from const import (
    ES_HOST,
    ES_PORT
)

es = Elasticsearch(host=ES_HOST, port=ES_PORT)
es = Elasticsearch()


# you need search in particular field and keyword must be word, not letter
def full_text_search(keyword, index, field):
    res = es.search(
        index=index,
        body={
            "query": {
                "match": {
                    field: keyword
                }
            }
        }
    )
    return res


def regex_search(pat, index, field):
    res = es.search(
        index=index,
        body={
            "query": {
                "regexp": {
                    field: pat
                }
            }
        }
    )
    return res


def prefix_search(prefix, index, field):
    res = es.search(
        index=index,
        body={
            "query": {
                "prefix": {
                    field: prefix
                }
            }
        }
    )
    return res


if __name__ == "__main__":
    index = "test-index"
    keyword = "Female"
    field = "gender"
    regex_pat = ".*?e.+"
    prefix = "ma"
    res = full_text_search(keyword, index, field)
    res = regex_search(regex_pat, index, field)
    res = prefix_search(prefix, index, field)
    # print(res)
