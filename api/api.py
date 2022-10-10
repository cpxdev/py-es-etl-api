from flask import Flask
from employee_api import employee_api

app = Flask(__name__)
app.register_blueprint(employee_api)

if __name__ == "__main__":
    app.run(debug=True)
