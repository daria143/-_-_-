from flask import Flask
from flask_restful import Api, Resource
import pyorient
import requests
import time

password  = "popa2704"
add_condition = " (NOT (in = "+'"' + '#34:0' + '"))' + " AND( NOT( in = " + '"' + '#34:1' + '"))'
app = Flask(__name__)
api = Api()
app.debug = True
db_name = 'db_Bank'
client = pyorient.OrientDB("localhost",2424)
client.set_session_token(True)
client.connect("root", password)
client.db_open(db_name, "root", password)


def home(dataList):
    start_time = time.process_time()
    keywords = dataList[1]['keyword']
    conditionText = ''

    for i in range(len(keywords)):
        conditionText = conditionText + "out.name = " + '"' + keywords[i].capitalize() + '"'
        if i != len(keywords) - 1:
            conditionText = conditionText + " OR "

    if conditionText != '':
        conditionText = "WHERE (" + conditionText + ")"

    result = client.command("Select out.name as sub_name, in.name as name from data_pk " + conditionText + " AND " + add_condition)
    Second = False
    if len(result) == 0:
        result = client.command("Select out.name as sub_name, in.name as name, value_param as value from data_value " + conditionText + " Order by sub_name")
        Second = True
    Third = False
    if len(result) == 0:
        Second = False
        result = client.command("Select name from data_kind")
        Third = True
    res = {}
    for i in range(len(result)):
        lst = []
        lst.append({"name":result[i].name})
        if not Second:
            lst.append({"value":""})
        else:
            lst.append({"value":result[i].value})
        if not Third:
            lst.append({"sub_name" : result[i].sub_name})
        else:
            lst.append({"sub_name": ""})

        res[i] = lst
    print(str(time.process_time() - start_time) + " секунд")
    return res


class Main(Resource):
    def get(self, problem_id, user_id):
        res = requests.get(url="http://127.0.0.1:3001/api/translate_q/"+ str(user_id)+"/"+str(problem_id))
        result = home(res.json())
        return result

    def post(self, problem_id):
        return db_name

api.add_resource(Main, "/api/found/<int:user_id>/<int:problem_id>")
api.init_app(app)

app.run(debug=True, port=3002, host="127.0.0.1")

