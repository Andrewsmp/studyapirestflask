from flask import Flask, request, jsonify
import json

app = Flask(__name__)

tasks=[{'id': 1, 'owner': 'Andrews','task': 'Building a API of tasks', 'status': 'pending'},
       {'id': 2, 'owner': 'Boby','task': 'Start a diet', 'status': 'pending'}]

@app.route('/task/<int:position>/', methods=['GET', 'PUT', 'DELETE'])
def task(position):

    if request.method == 'GET':
        try:
            response = tasks[position]
        except IndexError:
            response = {'status': 'error','message': 'Has no task with ID {}'.format(position)}
        except Exception:
            response = {'status': 'error','message': 'Unknown error. Please contact API administrator'}
        return jsonify(response)

    if request.method == 'PUT':
        data = json.loads(request.data)
        if data['status'] == 'done' or data['status'] == 'pending':
            tasks[position]['status'] = data['status']
            return jsonify({'status': 'sucess', 'message': 'update status task'})
        return jsonify({'status': 'error',
        'message': "You can only change " 
        + "the status of the task and the status must be 'done' or 'pending'"})
            
    if request.method == 'DELETE':
        del(tasks[position])
        return jsonify({'status': 'sucess', 'message': 'record deleted'})

def generate_id():
    return tasks[len(tasks)-1]['id'] + 1
    
@app.route('/task/', methods=['GET', 'POST'])
def list_tasks():

    if request.method == 'GET':
        return jsonify(tasks)

    if request.method == 'POST':
        data = json.loads(request.data)
        data['id'] = generate_id()
        tasks.append(data)
        return jsonify({'status': 'sucess', 'message': 'inserted task'})

if __name__=='__main__':
    app.run(debug=True)