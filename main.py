from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api()

problems = {1: {"question_id": 255, "question": "Хочу узнать по поводу кредита для пенсионеров"},
           2: {"question_id": 256, "question": "Я звоню узнать по поводу льготной ипотеки для it-специалистов"}}


class Main(Resource):
    def get(self, problem_id):
        if problem_id == 0:
            return problems
        else:
            return problems[problem_id]

    def post(self, problem_id):
        parser = reqparse.RequestParser()
        parser.add_argument("question_id", type=int)
        parser.add_argument("question", type=str)
        problems[problem_id] = parser.parse_args()
        return problems


api.add_resource(Main, "/api/problems/<int:problem_id>")
api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="127.0.0.1")