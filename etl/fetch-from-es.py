from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch(host='localhost', port=9200)
es = Elasticsearch(hosts="http://elastic:ZiFepQOGsi6giLCgoxqM@localhost:9200/")


if __name__ == "__main__":
    try:
        index_name = 'earth-finance-employee-details'   
        if es.indices.exists(index=index_name): 
            print("Index with name ", index_name , " already exist")
        else:    
            print("Creating a new index with name ", index_name)
            #es.indices.delete(index=index_name, ignore=[400, 404])
            es.indices.create(index=index_name, ignore=400)        
       
        search_param = {         
            "terms": {
                "HRID": [ "777" ]
             }           
        }
        response = es.search(index=index_name, query=search_param)
        print(response)
        
    except Exception as e:
        print("\nERROR:", e)
