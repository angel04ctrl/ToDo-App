from flask import Flask, render_template, request, jsonify
import grpc
import todo_pb2
import todo_pb2_grpc

app = Flask(__name__)

# Canal gRPC (ahora apunta al puerto correcto)
channel = grpc.insecure_channel('localhost:50051')
stub = todo_pb2_grpc.TodoServiceStub(channel)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/todos', methods=['GET'])
def get_todos():
    response = stub.ListTodos(todo_pb2.Empty())
    todos = [{"id": t.id, "title": t.title, "completed": t.completed} for t in response.todos]
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    response = stub.CreateTodo(todo_pb2.CreateTodoRequest(title=data['title']))
    return jsonify({"id": response.id, "title": response.title, "completed": response.completed})

@app.route('/api/todos/<string:tid>/toggle', methods=['POST'])
def toggle_todo(tid):
    response = stub.ToggleComplete(todo_pb2.TodoIdRequest(id=tid))
    return jsonify({"id": response.id, "title": response.title, "completed": response.completed})

@app.route('/api/todos/<string:tid>', methods=['DELETE'])
def delete_todo(tid):
    stub.DeleteTodo(todo_pb2.TodoIdRequest(id=tid))
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)