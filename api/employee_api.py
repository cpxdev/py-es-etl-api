from flask import Flask, request, jsonify, make_response
from flask import Blueprint
from employee_crud import EmployeeCRUD
from api_response import APIResponse

employee_api = Blueprint('employee_api', __name__)
emp_crud = EmployeeCRUD()
response = APIResponse()

@employee_api.route('/api/v1/employees', methods=['GET'])
def index():  
    document = emp_crud.search_employee(None, None)
    return make_response(response.build_search_response(document))


@employee_api.route('/api/v1/employees/<id>', methods=['GET'])
def search_employee(id):
    document = emp_crud.search_employee("HRID", id)
    return make_response(response.build_search_response(document))


@employee_api.route('/api/v1/employees', methods=['POST'])
def insert_new_employee():
    document = emp_crud.insert_new_employee(request.get_json());
    return make_response(response.build_insert_response(document))


@employee_api.route('/api/v1/employees/bulk', methods=['POST'])
def insert_bulk_employees():
    res = emp_crud.insert_bulk_employees(request.get_json());
    return make_response(response.build_bulk_insert_response(res))


@employee_api.route('/api/v1/employees/<id>', methods=['DELETE'])
def delete_employee(id):
    res = emp_crud.delete_employee("HRID", id)
    return make_response(response.build_delete_response(res['deleted']))


@employee_api.route('/api/v1/employees', methods=['DELETE'])
def delete_all_employees():
    res = emp_crud.delete_all_employees();
    return make_response(response.build_delete_response(res['deleted']))

"""
@employee_api.route('/api/v1/employees/<hrid>', methods=['DELETE'])
def delete_employee_by_hrid(hrid):
    query = {
        "query": {
            "terms": {
                "HRID": [ hrid ]
            }
        }
    }
    response = es.delete_by_query(index = finance_emp_index, body = query)
    return make_response(jsonify({"employee": response}))
"""
