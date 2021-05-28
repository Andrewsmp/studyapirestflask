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
            response = {'status': 'error','message': 'Has no task with ID {}'.format(position)}
        except Exception:
            response = {'status': 'error','message': 'Unknown error. Please contact API administrator'}
        return response

    def put(self, position):
        data = json.loads(request.data)
        if data['status'] == 'done' or data['status'] == 'pending':
            tasks[position]['status'] = data['status']
            return {'status': 'sucess', 'message': 'update status task'}
        return {'status': 'error',
        'message': "You can only change " 
        + "the status of the task and the status must be 'done' or 'pending'"}
            
    def delete(self, position):
        del(tasks[position])
        return {'status': 'sucess', 'message': 'record deleted'}

def generate_id():
        return tasks[len(tasks)-1]['id'] + 1

class List_All_Tasks(Resource):

    def get(self):
        return tasks

    def post(self):
        data = json.loads(request.data)
        data['id'] = generate_id()
        tasks.append(data)
        return {'status': 'sucess', 'message': 'inserted task'}

api.add_resource(Task, '/task/<int:position>/')
api.add_resource(List_All_Tasks, '/task/')

if __name__=='__main__':
    app.run(debug=True)