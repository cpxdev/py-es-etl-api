from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import pandas as pd

es = Elasticsearch(host='localhost', port=9200)
es = Elasticsearch()

def get_data_from_elastic():
    # query: The elasticsearch query.
    query = {
        "query": {
            "match": {
                "products": "Nice Product"
            }
        }
    }

    # Scan function to get all the data. 
    rel = scan(client=es,             
               query=query,                                     
               scroll='1m',
               index='products',
               raise_on_error=True,
               preserve_order=False,
               clear_scroll=True)

    # Keep response in a list.
    result = list(rel)

    temp = []

    # We need only '_source', which has all the fields required.
    # This elimantes the elasticsearch metdata like _id, _type, _index.
    for hit in result:
        temp.append(hit['_source'])

    # Create a dataframe.
    df = pd.DataFrame(temp)

    return df


df = get_data_from_elastic()

print(df.head())