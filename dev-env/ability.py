from flask_restful import Resource
from flask import request
import json

list_abilities = ['Python', 'Php', 'Java', 'Ruby', 'Javascript', 'Css', 'Html', 'C#',
                  'Go', 'Ruby On Rails', 'Flask', 'Flask Restful', 'Django', 'Spring',
                  'Api']

class Abilities(Resource):

    def get(self, position):
        try:
            return list_abilities[position]
        except IndexError:
            return {'status': 'error', 'message': 'Has no skill in this position.'}

    def put(self, position):
        try:
            data = json.loads(request.data)
            data = data[0].title()
            if data not in list_abilities:
                list_abilities[position] = data
            return {'status': 'success', 'message': 'Altered skill'}
        except IndexError:
            return {'staus': 'esrror', 'message': 'Has no skill in this position.'}

    def delete(self, position):
        try:
            del(list_abilities[position])
            return {'status': 'success', 'message': 'Deleted skill'}
        except IndexError:
            return {'staus': 'error', 'message': 'Has no skill in this position.'}

class ListAllAbilities(Resource):

    def get(self):
        return list_abilities

    def post(self):
        data = json.loads(request.data)
        data = [x.title() for x in data if x.title() not in list_abilities]
        for item in data:
            list_abilities.append(item)
        return {'status': 'success', 'message': 'Skills added'}