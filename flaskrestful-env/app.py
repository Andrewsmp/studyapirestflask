from flask import Flask, request
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

tasks=[{'id': 1, 'owner': 'Andrews','task': 'Building a API of tasks', 'status': 'pending'},
       {'id': 2, 'owner': 'Boby','task': 'Start a diet', 'status': 'pending'}]

class Task(Resource):

    def get(self, position):
        try:
            response = tasks[position]
        except IndexError:
            response = {'status': 'error','message': 'Has no task in this position'}
        except Exception:
            response = {'status': 'error','message': 'Unknown error. Please contact API administrator'}
        return response

    def put(self, position):
        try:
            data = json.loads(request.data)
            if (data == 'done' or data == 'pending') and data != tasks[position]['status']:
                tasks[position]['status'] = data
                return {'status': 'success', 'message': 'update status task'}
        except IndexError:
            return {'status': 'error', 'message': 'Has no task in this position'}
        return {'status': 'error',
        'message': "You can only change " 
        + "the status of the task and the status must be 'done' or 'pending'"}
            
    def delete(self, position):
        try:
            del(tasks[position])
            return {'status': 'success', 'message': 'record deleted'}
        except IndexError:
            return {'status': 'error', 'message': 'Has no task in this position'}

class List_All_Tasks(Resource):

    def get(self):
        return tasks

    def post(self):
        data = json.loads(request.data)
        data['id'] = tasks[len(tasks)-1]['id'] + 1
        tasks.append(data)
        return {'status': 'success', 'message': 'inserted task'}

api.add_resource(Task, '/task/<int:position>/')
api.add_resource(List_All_Tasks, '/task/')

if __name__=='__main__':
    app.run(debug=True)