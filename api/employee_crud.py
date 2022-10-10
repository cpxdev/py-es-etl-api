from elasticsearch import Elasticsearch
from elasticsearch import helpers

  

class EmployeeCRUD(object):
    def __init__(self):
        #es = Elasticsearch(['http://localhost:9200'], http_auth=('elastic', 'ZiFepQOGsi6giLCgoxqM'))
        #es = Elasticsearch([{'host': 'localhost', 'port': '9200'}], http_auth=('elastic', 'ZiFepQOGsi6giLCgoxqM'))
        #es = Elasticsearch(host='localhost', port=9200)
        self.es = Elasticsearch(hosts="http://elastic:ZiFepQOGsi6giLCgoxqM@localhost:9200/")
        self.finance_emp_index = 'earth-finance-employee-details' 

    def insert_new_employee(self, employee):
    
        res = self.es.index(index=self.finance_emp_index, doc_type="employee_details", body=employee)
        res = self.es.get(index=self.finance_emp_index, doc_type='employee_details', id=res['_id'])  
        self.es.indices.refresh(index=self.finance_emp_index)
        
        return res

    def insert_bulk_employees(self, employees):
    
        actions = []
        for employee in employees:
            doc ={
                '_op_type': 'index',
                '_index': self.finance_emp_index,               
                '_source': employee
            }
            actions.append(doc)
         
        #res = self.es.bulk(index=self.finance_emp_index, action=actions)
        res = helpers.bulk(self.es, actions)
        return res
        
    def search_employee(self, what, query):
        if what is None:
            res = self.es.search(index=self.finance_emp_index, body={"query": {"match_all": {}}})
        else:
            res = self.es.search(index=self.finance_emp_index, body={"query": {"match": {what: query}}})
        
        documents = []
        for hit in res['hits']['hits']:         
            documents.append(hit['_source'])
            
        return documents

    def delete_employee(self, what, query):
        res = self.es.delete_by_query(index=self.finance_emp_index, body={"query": {"match": {what: query}}}) #{"match_all": {}}
        return res
        
    def delete_all_employees(self):
        res = self.es.delete_by_query(index=self.finance_emp_index, body={"query": {"match_all": {}}}) #{"match_all": {}}
        return res