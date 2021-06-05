from flask import Flask, request
from flask_restful import Resource, Api
import json
from models import Person, Activity

app = Flask(__name__)
api = Api(app)

class PersonApi(Resource):
    
    def get(self, id):
        person = Person.query.filter_by(id=id).first()
        try:
            response ={
                'id': person.id,
                'name': person.name,
                'age': person.age
            }
        except AttributeError:
            response = {'status': 'error', 'message': 'Person not found'}
        except Exception:
            response = {'status': 'error', 'message': 'Unexpected error'}
        return response

    #modify the person's name or age or both
    def put(self, id):
        data = json.loads(request.data)
        person = Person.query.filter_by(id=id).first()
        try:
            if 'name' in data:
                person.name = data['name']
            if 'age' in data:
                person.age = data['age']
            person.save()
            response = {
                'id': person.id,
                'name': person.name,
                'age': person.age
            }
        except AttributeError:
            response = {'status': 'error', 'message': 'Person not found'}
        except Exception:
            response = {'status': 'error', 'message': 'Unexpected error'}
        return response

    #removes a person but checks if they have any activity and removes them before
    def delete(self, id):
        person = Person.query.filter_by(id=id).first()
        activities = Activity.query.filter_by(person_id=id)
        if len(list(activities)) != 0:
            for item in activities:
                item.remove()
        try:
            person.remove()
            response = {'status': 'success', 'message': 'Deleted person'}
        except AttributeError:
            response = {'status': 'error', 'message': 'Person not found'}
        except Exception:
            response = {'status': 'error', 'message': 'Unexpected error'}
        return response

class ListPerson(Resource):

    def get(self):
        people = Person.query.all()
        response = [{'id': i.id, 'name': i.name, 'age': i.age} for i in people]
        return response

    def post(self):
        data = json.loads(request.data)
        try:
            person = Person(name=data['name'], age=data['age'])
            person.save()
            response = {
                'id': person.id,
                'name': person.name,
                'age': person.age
            }
        except KeyError:
            response = {'status': 'error', 'message': 'Incorrect key'}
        except Exception:
            response = {'status': 'error', 'message': 'Unexpected error'}
        return response

class ListActivity(Resource):

    #returns a list of all activities
    def get(self):
        data = Activity.query.all()
        response = [{'id': i.id, 
                     'name': i.name,
                     'status': i.status,
                     'person': i.person.name,
                     'person_id': i.person_id} 
                     for i in data]
        return response

    #creates a new activity handling its status
    def post(self):
        data = json.loads(request.data)
        if data['status'] == 'pending' or data['status'] == 'done':
            try:
                person = Person.query.filter_by(name=data['person']).first()
                activity = Activity(name=data['name'], status=data['status'],person=person)
                activity.save()
                response = {
                    'id': activity.id,
                    'name': activity.name,
                    'status': activity.status,
                    'person': activity.person.name,
                    'person_id': activity.person_id
                }
            except KeyError:
                response = {'status': 'error', 'message': 'Incorrect key'}
            except AttributeError:
                response = {'status': 'error', 'message': "Person's name is wrong"}
            except Exception:
                response = {'status': 'error', 'message': 'Unexpected error'}
        else:
            response = {'status': 'error', 'message': 'Status must be pending or done'}
        return response

class ActivityApi(Resource):

    #returns all activities of a person through the id of the person sent
    def get(self, id):
        activities = Activity.query.filter_by(person_id=id)
        if len(list(activities)) != 0:
            response = [{'id': i.id, 
                        'name': i.name,
                        'status': i.status,
                        'person': i.person.name,
                        'person_id': i.person_id} 
                        for i in activities]
        else:
            response = {'status': 'error', 'message': 'Activities list not found'}
        return response

    #modify activity status or name via activity id
    def put(self, id):
        activity = Activity.query.filter_by(id=id).first()
        data = json.loads(request.data)
        if 'name' in data:
            activity.name = data['name']
        else:
            return {'status': 'error', 'message': 'Key error'}
        if 'status' in data and (data['status'] == 'pending' or data['status'] == 'done'):
            activity.status = data['status']
        else:
            return {'status': 'error', 'message': 'Status must be pending or done'}
        activity.save()
        response = {
            'id': activity.id,
            'name': activity.name,
            'status': activity.status,
            'person': activity.person.name,
            'person_id': activity.person_id
        }
        return response

    #remove an activity via its id
    def delete(self, id):
        activity = Activity.query.filter_by(id=id).first()
        try:
            activity.remove()
            response = {'status': 'success', 'message': 'Deleted activity'}
        except AttributeError:
            response = {'status': 'error', 'message': 'Activity not found'}
        except Exception:
            response = {'status': 'error', 'message': 'Unexpected error'}
        return response

api.add_resource(PersonApi, '/person/<int:id>/')
api.add_resource(ListPerson, '/person/')
api.add_resource(ListActivity, '/activity/')
api.add_resource(ActivityApi, '/activity/<int:id>/')

if __name__=='__main__':
    app.run(debug=True)