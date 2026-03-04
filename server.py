import grpc
from concurrent import futures
import uuid
import sqlite3
from datetime import datetime
import todo_pb2
import todo_pb2_grpc

class TodoServicer(todo_pb2_grpc.TodoServiceServicer):
    def __init__(self):
        self.conn = sqlite3.connect('todos.db', check_same_thread=False)
        self.create_table()

    def create_table(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS todos (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT,
            due_date TEXT,
            completed INTEGER DEFAULT 0,
            created_at TEXT
        )''')
        self.conn.commit()

    def CreateTodo(self, request, context):
        todo_id = str(uuid.uuid4())
        created_at = datetime.now().isoformat()
        self.conn.execute('''INSERT INTO todos (id, title, description, priority, due_date, completed, created_at)
                             VALUES (?, ?, ?, ?, ?, ?, ?)''',
                          (todo_id, request.title, request.description, request.priority, request.due_date, 0, created_at))
        self.conn.commit()
        return self._get_todo(todo_id)

    def ListTodos(self, request, context):
        cursor = self.conn.execute("SELECT * FROM todos ORDER BY due_date ASC, priority DESC")
        todos = [self._row_to_proto(row) for row in cursor]
        return todo_pb2.TodoList(todos=todos)

    def ToggleComplete(self, request, context):
        self.conn.execute("UPDATE todos SET completed = NOT completed WHERE id = ?", (request.id,))
        self.conn.commit()
        return self._get_todo(request.id)

    def DeleteTodo(self, request, context):
        self.conn.execute("DELETE FROM todos WHERE id = ?", (request.id,))
        self.conn.commit()
        return todo_pb2.Empty()

    def UpdateTodo(self, request, context):
        self.conn.execute('''UPDATE todos SET title=?, description=?, priority=?, due_date=?, completed=? WHERE id=?''',
                          (request.title, request.description, request.priority, request.due_date, int(request.completed), request.id))
        self.conn.commit()
        return self._get_todo(request.id)

    def _get_todo(self, todo_id):
        cursor = self.conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()
        if not row:
            context.abort(grpc.StatusCode.NOT_FOUND, "Tarea no encontrada")
        return self._row_to_proto(row)

    def _row_to_proto(self, row):
        return todo_pb2.Todo(
            id=row[0],
            title=row[1],
            description=row[2] or "",
            priority=row[3] or "Media",
            due_date=row[4] or "",
            completed=bool(row[5]),
            created_at=row[6]
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todo_pb2_grpc.add_TodoServiceServicer_to_server(TodoServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("✅ Servidor gRPC PRO corriendo en http://localhost:50051 (SQLite)")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()