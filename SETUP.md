# 📋 ToDo-App — Guía de instalación, ejecución y uso

Aplicación de tareas con arquitectura **Flask + gRPC + SQLite**.

## 1) Qué cambió en esta versión

Novedades ya implementadas en el código actual:

- Persistencia en **SQLite** (`todos.db`) en lugar de almacenamiento en memoria.
- Modelo de tarea extendido con:
  - `title`
  - `description`
  - `priority` (`Alta`, `Media`, `Baja`)
  - `due_date` (formato `YYYY-MM-DD`)
  - `completed`
  - `created_at`
- Nuevo endpoint REST para edición: **`PUT /api/todos/<id>`**.
- Nuevo RPC gRPC: **`UpdateTodo`**.
- Frontend con:
  - Filtros (`Todas`, `Pendientes`, `Completadas`)
  - Modal de edición
  - Estadísticas (total/completadas/pendientes)
  - Auto-refresh cada 3 segundos

## 2) Estructura del proyecto

```text
ToDo-App/
├── app.py                 # Servidor Flask (API REST + UI)
├── server.py              # Servidor gRPC + SQLite
├── todo.proto             # Contrato gRPC
├── todo_pb2.py            # Mensajes Protobuf generados
├── todo_pb2_grpc.py       # Stubs gRPC generados
├── templates/
│   └── index.html         # Interfaz web
├── requirements.txt
├── run.sh                 # Arranque automático Mac/Linux
├── run.ps1                # Arranque automático Windows
└── SETUP.md
```

## 3) Requisitos

- Python 3.9+
- pip
- ngrok (opcional)

## 4) Instalación

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Si PowerShell bloquea scripts:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## 5) Ejecución en un solo paso (recomendado)

### macOS / Linux

```bash
chmod +x run.sh
./run.sh
```

### Windows

```powershell
powershell -ExecutionPolicy Bypass -File run.ps1
```

Los scripts:

1. Validan que estés en la raíz del proyecto.
2. Activan `venv` (o lo crean si no existe).
3. Levantan:
   - gRPC server en `50051`
   - Flask app en `5000`
4. Preguntan si quieres abrir ngrok.

## 6) Ejecución manual

### Terminal 1: gRPC

```bash
source venv/bin/activate
python3 server.py
```

Salida esperada:

```text
✅ Servidor gRPC PRO corriendo en http://localhost:50051 (SQLite)
```

### Terminal 2: Flask

```bash
source venv/bin/activate
python3 app.py
```

Abrir en navegador:

- http://localhost:5000

## 7) API REST actual

### `GET /api/todos`
Lista tareas.

### `POST /api/todos`
Crea una tarea.

Body de ejemplo:

```json
{
  "title": "Preparar demo",
  "description": "Subir cambios y verificar endpoints",
  "priority": "Alta",
  "due_date": "2026-03-10"
}
```

### `PUT /api/todos/<id>`
Edita una tarea existente.

Body de ejemplo:

```json
{
  "title": "Preparar demo final",
  "description": "Con checklist",
  "priority": "Media",
  "due_date": "2026-03-12",
  "completed": false
}
```

### `POST /api/todos/<id>/toggle`
Alterna estado completado.

### `DELETE /api/todos/<id>`
Elimina tarea.

### Respuesta tipo de una tarea

```json
{
  "id": "uuid",
  "title": "Preparar demo",
  "description": "Subir cambios",
  "priority": "Alta",
  "due_date": "2026-03-10",
  "completed": false,
  "created_at": "2026-03-04T14:30:00.000000"
}
```

## 8) Servicios gRPC actuales (`todo.proto`)

- `CreateTodo(CreateTodoRequest) returns (Todo)`
- `ListTodos(Empty) returns (TodoList)`
- `ToggleComplete(TodoIdRequest) returns (Todo)`
- `DeleteTodo(TodoIdRequest) returns (Empty)`
- `UpdateTodo(UpdateTodoRequest) returns (Todo)`

Campos principales:

- `CreateTodoRequest`: `title`, `description`, `priority`, `due_date`
- `UpdateTodoRequest`: `id`, `title`, `description`, `priority`, `due_date`, `completed`
- `Todo`: `id`, `title`, `description`, `priority`, `due_date`, `completed`, `created_at`

## 9) Base de datos (SQLite)

- Archivo local: `todos.db`
- Tabla: `todos`
- Se crea automáticamente al arrancar `server.py`.
- Orden de listado en backend:
  - `due_date ASC`
  - `priority DESC`

## 10) ngrok (opcional)

Con la app corriendo en `5000`:

```bash
ngrok http 5000
```

Comparte la URL `https://...ngrok-free.app`.

## 11) Regenerar Protobuf (si cambias `todo.proto`)

```bash
source venv/bin/activate
python -m grpc_tools.protoc \
  -I. \
  --python_out=. \
  --grpc_python_out=. \
  todo.proto
```

## 12) Troubleshooting

### VS Code marca warning en `grpc` o `flask`

Selecciona el intérprete del venv:

- `Python: Select Interpreter`
- Elegir `./venv/bin/python` (o `venv\Scripts\python.exe` en Windows)

### Flask no conecta con gRPC

- Verifica que `server.py` esté corriendo en `50051`.
- Inicia primero gRPC y luego Flask.

### Puerto ocupado

macOS/Linux:

```bash
lsof -i :5000
lsof -i :50051
```

Windows:

```powershell
netstat -ano | findstr :5000
netstat -ano | findstr :50051
```

### Reinicio limpio

- Detén procesos (`Ctrl+C`).
- Vuelve a ejecutar `./run.sh` o `run.ps1`.

---

Si agregas nuevas funcionalidades, actualiza este archivo en la sección **“Qué cambió en esta versión”** y en **API REST / gRPC** para mantener la documentación alineada con el código.