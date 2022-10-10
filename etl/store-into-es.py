from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json
import pandas as pd

es = Elasticsearch(host='localhost', port=9200)
es = Elasticsearch(hosts="http://elastic:ZiFepQOGsi6giLCgoxqM@localhost:9200/")


def excel_to_json(file_name):
    excel_data_df = pd.read_excel(file_name, skiprows=[0])
    json_str = excel_data_df.to_json(orient='records')
    json_records = json.loads(json_str)  
    return json_records
            
def insert_data_into_es(file_name): 
    try:
        print("Adding new records from file ", file_name)
        json_records = excel_to_json(file_name)
        action_list = []
        for row in json_records:
            record ={
                '_op_type': 'index',
                '_index': index_name,               
                '_source': row
            }
            action_list.append(record)
            
        response = helpers.bulk(es, action_list)
        print ("\nActions RESPONSE:", response)
    except Exception as e:
        print("\nERROR:", e)


if __name__ == "__main__":
    try:
        index_name = 'earth-finance-employee-details'   
        if es.indices.exists(index=index_name): 
            print("Index with name ", index_name , " already exist")
        else:    
            print("Creating a new index with name ", index_name)
            #es.indices.delete(index=index_name, ignore=[400, 404])
            es.indices.create(index=index_name, ignore=400)
        
        insert_data_into_es('../data/Earth Finance Employee Details.xlsx')
        
    except Exception as e:
        print("\nERROR:", e)
