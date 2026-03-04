from flask import Flask, render_template, request, jsonify
import grpc
import todo_pb2
import todo_pb2_grpc

app = Flask(__name__)

channel = grpc.insecure_channel('localhost:50051')
stub = todo_pb2_grpc.TodoServiceStub(channel)

@app.route('/')
def index():
    return render_template('index.html')

# === API REST ===
@app.route('/api/todos', methods=['GET'])
def get_todos():
    response = stub.ListTodos(todo_pb2.Empty())
    todos = [todo_to_dict(t) for t in response.todos]
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    response = stub.CreateTodo(todo_pb2.CreateTodoRequest(
        title=data['title'],
        description=data.get('description', ''),
        priority=data.get('priority', 'Media'),
        due_date=data.get('due_date', '')
    ))
    return jsonify(todo_to_dict(response))

@app.route('/api/todos/<string:tid>', methods=['PUT'])
def update_todo(tid):
    data = request.get_json()
    response = stub.UpdateTodo(todo_pb2.UpdateTodoRequest(
        id=tid,
        title=data['title'],
        description=data.get('description', ''),
        priority=data.get('priority', 'Media'),
        due_date=data.get('due_date', ''),
        completed=data.get('completed', False)
    ))
    return jsonify(todo_to_dict(response))

@app.route('/api/todos/<string:tid>/toggle', methods=['POST'])
def toggle_todo(tid):
    response = stub.ToggleComplete(todo_pb2.TodoIdRequest(id=tid))
    return jsonify(todo_to_dict(response))

@app.route('/api/todos/<string:tid>', methods=['DELETE'])
def delete_todo(tid):
    stub.DeleteTodo(todo_pb2.TodoIdRequest(id=tid))
    return jsonify({"success": True})

def todo_to_dict(t):
    return {
        "id": t.id, "title": t.title, "description": t.description,
        "priority": t.priority, "due_date": t.due_date,
        "completed": t.completed, "created_at": t.created_at
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)