import grpc
from concurrent import futures
import uuid
import todo_pb2
import todo_pb2_grpc

class TodoServicer(todo_pb2_grpc.TodoServiceServicer):
    def __init__(self):
        self.todos = {}   # base de datos en memoria

    def CreateTodo(self, request, context):
        todo_id = str(uuid.uuid4())
        todo = todo_pb2.Todo(id=todo_id, title=request.title, completed=False)
        self.todos[todo_id] = todo
        return todo

    def ListTodos(self, request, context):
        return todo_pb2.TodoList(todos=self.todos.values())

    def ToggleComplete(self, request, context):
        if request.id not in self.todos:
            context.abort(grpc.StatusCode.NOT_FOUND, "Tarea no encontrada")
        todo = self.todos[request.id]
        todo.completed = not todo.completed
        return todo

    def DeleteTodo(self, request, context):
        if request.id in self.todos:
            del self.todos[request.id]
        return todo_pb2.Empty()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todo_pb2_grpc.add_TodoServiceServicer_to_server(TodoServicer(), server)
    server.add_insecure_port('[::]:50051')   # ← CAMBIADO A 50051
    server.start()
    print("✅ Servidor gRPC corriendo en http://localhost:50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()