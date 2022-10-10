#encodings=utf-8
from flask import Flask, request, render_template, redirect
import sqlite3
from elasticsearch import Elasticsearch


class ES(object):
    def __init__(self):
        self.es = Elasticsearch()
        self.id = 0

    def insert_es(self, id, good, description):
        doc = {
            'id': id,
            'good': good,
            'description': description
            }
        res = self.es.index(index="test-index", doc_type='description_goods', id=self.id, body=doc)
        #print(res['created'])
        res = self.es.get(index="test-index", doc_type='description_goods', id=self.id)
        #print(res['_source'])
        self.es.indices.refresh(index="test-index")
        self.id += 1

    def search_es(self, what, query):
        res = self.es.search(index="test-index", body={"query": {"match": {what: query}}})  #"author": 'kimchy'
        print("Got %d Hits" % res['hits']['total'])
        documents = []
        for hit in res['hits']['hits']:
            #print(hit
            documents.append(hit['_source'])
        return documents

    def del_by_query(self, query):
        res = self.es.delete_by_query(index="test-index", body={"query": {"match": {query}}}) #{"match_all": {}}

    def del_all(self):
        res = self.es.delete_by_query(index="test-index", body={"query": {"match_all": {}}}) #{"match_all": {}}


class SQL(object):
    def __init__(self, test_db):
        self.connection = sqlite3.connect(test_db)
        self.cursor = self.connection.cursor()
        self.table = 'CREATE TABLE goods(id INTEGER, NAME TEXT, WEIGHT INTEGER, NUM INTEGER)'
        self.cursor.execute(self.table)
        #closed method
        #self.__data

    def insert(self, id, good, weight, num):
        query = 'INSERT into goods VALUES ({}, "{}", {}, {})'.format(id, good, weight, num)
        self.cursor.execute(query)
        self.connection.commit()

    def search_sql(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()


es = ES()
sql = SQL(':memory:')

app = Flask(__name__)
@app.route('/')
def index(): return render_template('index.html')

@app.route('/insert')
def fill_in_db():
    print('Filling ES database')
    es.insert_es(1, "Chair", "big")
    es.insert_es(2, "Table", 15)
    es.insert_es(3, "TV", 5)
    es.insert_es(8, "Bed", 15)
    es.insert_es(10, "Chair", 10)

    print('Filling SQL database')
    sql.insert(1, "Chair", 15, 33)
    sql.insert(1, "Table1", 20, 17)

    print('All databases are filled in')
    return redirect('/search_form')

def execute_query(q):
    query = u'SELECT * FROM goods WHERE id={}'.format(q)
    f = sql.search_sql(query)
    print(f)
    return f

@app.route('/search_form')
def flask_search():
    found = []
    if request.args:
        for k, v in request.args.items():
            if v:
                scores = es.search_es(k, v)
                for d in scores:
                    for key, value in d.items():
                        if key == u'id':
                            f = execute_query(value)
                            for i in f:
                                print(i)
                                found.append(i)
    return render_template('form.html', found=found)

@app.route('/delete_all_es')
def delete_all_es():
    es.del_all()
    print('All data deleted')
    return redirect('/search_form')


if __name__ == '__main__':
    app.run(host='0.0.0.0')