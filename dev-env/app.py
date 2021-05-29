from flask import Flask, request
from flask_restful import Resource, Api
from ability import Abilities, ListAllAbilities, list_abilities
import json

app = Flask(__name__)
api = Api(app)

developers = [{'id': 1, 'name': 'Andrews', 'skills': ['Python', 'Flask', 'Java']},
              {'id': 2, 'name': 'Brian', 'skills': ['Api', 'Django', 'Java']}]

#this method validates if the sent skills contain in the list of skills
def validate_list(list):
    count = 0
    for i,item in enumerate(list):
        item = item.title()
        if item in list_abilities:
            list[i] = item
            count += 1
    if count == len(list):
        return True

class Developer(Resource):

    def get(self, position):
        try:
            response = developers[position]
        except IndexError:
            response = {'status': 'error', 'message': 'Has no developer in this position.'}
        except Exception:
            response = {'status': 'error', 'message': 'Unknown error.' + 
                        'Plesase contact API administrator.'}
        return response
    
    def put(self, position):
        try:
            data = json.loads(request.data)
            #calls the validate_list method to check if the skills sent are in the skills list
            if validate_list(data['skills']):
                developers[position]['name'] = data['name']
                developers[position]['skills'] = data['skills']
                return {'status': 'success', 'message': 'Update developer name and skills'}
            return {'status': 'error', 'message': 'All skills must contain in the list of skills'}
        except IndexError:
            return {'status': 'error', 'message': 'Developer in this position not exist.'}

    def delete(self, position):
        try:
            del(developers[position])
            return {'status': 'success', 'message': 'Deleted developer'}
        except IndexError:
            return {'status': 'error', 'message': 'Developer in this position not exist.'}

class ListAllDevelopers(Resource):
    
    def get(self):
        return developers

    def post(self):
        data = json.loads(request.data)
        #calls the validate_list method to check if the skills sent are in the skills list
        if validate_list(data['skills']):
            #generates a new id based adding +1 to the last id in the list
            data['id'] = developers[len(developers)-1]['id'] + 1
            developers.append(data)
            return {'status': 'success', 'message': 'Developer included'}
        return {'status': 'error', 'message': 'All skills must contain in the list of skills'}

api.add_resource(Developer, '/dev/<int:position>/')
api.add_resource(ListAllDevelopers, '/dev/')
api.add_resource(ListAllAbilities, '/abilities/')
api.add_resource(Abilities, '/abilities/<int:position>/')

if __name__=='__main__':
    app.run(debug=True)