from flask import Flask, request
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

developers = [{'id': 1, 'name': 'Andrews', 'skills': ['python', 'flask', 'java']},
              {'id': 2, 'name': 'Brian', 'skills': ['API', 'django', 'java']}]

class Developer(Resource):

    def get(self, position):
        try:
            response = developers[position]
        except IndexError:
            response = {'status': 'error', 'message': 'Has no developer whith in this position.'}
        except:
            response = {'status': 'error', 'message': 'Unknown error.' + 
                        'Plesase contact API administrator.'}
        return response
    
    def put(self, position):
        
        try:
            data = json.loads(request.data)
            if developers[position]['id'] == data['id']:
                developers[position]['name'] = data['name']
                developers[position]['skills'] = data['skills']
                return {'status': 'sucess', 'message': 'Update developer name and skills'}
            return {'status': 'error', 'message': 'It is not possible to ' + 
                    'change the ID.'}
        except IndexError:
            return {'status': 'error', 'message': 'Developer in this position not exist.'}

    def delete(self, position):
        del(developers[position])
        return {'status': 'sucess', 'message': 'Deleted developer'}

def generate_id():
    return developers[len(developers)-1]['id'] + 1

class List_All(Resource):
    
    def get(self):
        return developers

    def post(self):

        data = json.loads(request.data)
        data['id'] = generate_id()
        developers.append(data)
        return {'status': 'sucess', 'message': 'Developer included'}

api.add_resource(Developer, '/dev/<int:position>/')
api.add_resource(List_All, '/dev/')

if __name__=='__main__':
    app.run(debug=True)