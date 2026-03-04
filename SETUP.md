# 📋 ToDo-App - Guía Completa de Instalación y Uso

Aplicación de gestión de tareas con arquitectura cliente-servidor usando **gRPC** y **Flask**.

## 📁 Estructura del Proyecto

```text
ToDo-App/
├── app.py                 # Servidor Flask (frontend web)
├── server.py             # Servidor gRPC (backend)
├── todo.proto            # Definición Protocol Buffers
├── todo_pb2.py           # Código generado por protoc
├── todo_pb2_grpc.py      # Stubs gRPC generados
├── templates/
│   └── index.html        # Interfaz de usuario
├── requirements.txt      # Dependencias Python
├── run.sh               # Script de inicio (Mac/Linux)
├── run.ps1              # Script de inicio (Windows)
└── README.md            # Documentación básica
```

## 🏗️ Arquitectura

La aplicación utiliza una arquitectura de **microservicios** con comunicación gRPC:

```
┌─────────────┐      HTTP      ┌──────────────┐      gRPC       ┌──────────────┐
│   Browser   │ ◄────────────► │ Flask Server │ ◄─────────────► │ gRPC Server  │
│ (Frontend)  │                │  (puerto 5000)│                │ (puerto 50051)│
└─────────────┘                └──────────────┘                 └──────────────┘
```

### Componentes:

1. **gRPC Server** (`server.py`):
   - Escucha en `localhost:50051`
   - Gestiona la lógica de negocio
   - Almacena tareas en memoria
   - Operaciones: Crear, Listar, Alternar completado, Eliminar

2. **Flask Server** (`app.py`):
   - Escucha en `localhost:5000`
   - Cliente gRPC que se conecta al servidor
   - Expone API REST para el frontend
   - Sirve la interfaz HTML

3. **Protocol Buffers** (`todo.proto`):
   - Define la estructura de datos
   - Genera código para Python (`todo_pb2.py`, `todo_pb2_grpc.py`)

## 🔧 Requisitos Previos

- **Python 3.9+** (recomendado 3.10 o superior)
- **pip** actualizado
- **ngrok** (opcional, para acceso remoto)

## 📦 Instalación

### macOS / Linux

#### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd ToDo-App
```

#### 2. Crear entorno virtual
```bash
python3 -m venv venv
```

#### 3. Activar entorno virtual
```bash
source venv/bin/activate
```

#### 4. Instalar dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Windows

#### 1. Clonar el repositorio
```powershell
git clone <repository-url>
cd ToDo-App
```

#### 2. Crear entorno virtual
```powershell
python -m venv venv
```

#### 3. Activar entorno virtual

**PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

Si hay error de ejecución de scripts:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**CMD:**
```cmd
venv\Scripts\activate.bat
```

#### 4. Instalar dependencias
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 🚀 Ejecución Automática (Recomendado)

### macOS / Linux

#### Primera vez (dar permisos):
```bash
chmod +x run.sh
```

#### Ejecutar:
```bash
./run.sh
```

**Salida esperada:**
```
🚀 Iniciando ToDo-App...

✅ Entorno virtual activado
[1/3] Levantando gRPC Server en puerto 50051
gRPC PID: 12345
[2/3] Levantando Flask Server en puerto 5000
Flask PID: 12346
[3/3] ¿Quieres levantar ngrok para acceso remoto? (s/n)
```

- Responde **`n`** para uso local
- Responde **`s`** para exponer con ngrok

Si elegiste `n`:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Servidores activos:
   🔹 gRPC Server: http://localhost:50051
   🔹 Web App: http://localhost:5000
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Presiona Ctrl+C para detener los servidores
```

**Abre en el navegador:** http://localhost:5000

### Windows (PowerShell)

#### Ejecutar:
```powershell
powershell -ExecutionPolicy Bypass -File run.ps1
```

La salida y funcionamiento es idéntico a Mac/Linux.

## 🛠️ Ejecución Manual (Modo Desarrollo)

Si prefieres controlar cada proceso por separado:

### Terminal 1: Servidor gRPC
```bash
# Activar venv
source venv/bin/activate  # Mac/Linux
# .\venv\Scripts\Activate.ps1  # Windows PowerShell

# Iniciar servidor gRPC
python3 server.py
```

**Salida esperada:**
```
✅ Servidor gRPC corriendo en http://localhost:50051
```

### Terminal 2: Servidor Flask
```bash
# Activar venv
source venv/bin/activate  # Mac/Linux
# .\venv\Scripts\Activate.ps1  # Windows PowerShell

# Iniciar servidor Flask
python3 app.py
```

**Salida esperada:**
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### Terminal 3: ngrok (Opcional)
```bash
ngrok http 5000
```

**Salida esperada:**
```
Forwarding  https://abc-123-def.ngrok-free.app -> http://localhost:5000
```

Comparte la URL `https://...ngrok-free.app` para acceso remoto.

## 📖 Uso de la Aplicación

### Interfaz Web

Accede a http://localhost:5000 para ver la interfaz.

**Funcionalidades:**

1. **Agregar Tarea:**
   - Escribe en el campo de texto
   - Presiona "Add Task" o Enter

2. **Marcar como Completada:**
   - Haz clic en el checkbox junto a la tarea

3. **Eliminar Tarea:**
   - Haz clic en el botón "Delete"

4. **Estado en Tiempo Real:**
   - Las tareas se sincronizan automáticamente con el servidor gRPC

## 🔌 API REST Endpoints

El servidor Flask expone los siguientes endpoints:

### `GET /`
Renderiza la interfaz HTML principal.

### `GET /api/todos`
Lista todas las tareas.

**Respuesta:**
```json
[
  {
    "id": "uuid-1234",
    "title": "Comprar leche",
    "completed": false
  },
  {
    "id": "uuid-5678",
    "title": "Hacer ejercicio",
    "completed": true
  }
]
```

### `POST /api/todos`
Crea una nueva tarea.

**Request Body:**
```json
{
  "title": "Nueva tarea"
}
```

**Respuesta:**
```json
{
  "id": "uuid-9012",
  "title": "Nueva tarea",
  "completed": false
}
```

### `POST /api/todos/<id>/toggle`
Alterna el estado de completado de una tarea.

**Respuesta:**
```json
{
  "id": "uuid-1234",
  "title": "Comprar leche",
  "completed": true
}
```

### `DELETE /api/todos/<id>`
Elimina una tarea.

**Respuesta:**
```json
{
  "success": true
}
```

## 🧪 Pruebas Manuales con cURL

### Listar tareas
```bash
curl http://localhost:5000/api/todos
```

### Crear tarea
```bash
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Leer documentación"}'
```

### Alternar completado
```bash
curl -X POST http://localhost:5000/api/todos/<id>/toggle
```

### Eliminar tarea
```bash
curl -X DELETE http://localhost:5000/api/todos/<id>
```

## 🌐 Exposición con ngrok

### Instalación de ngrok

#### macOS
```bash
brew install ngrok
```

#### Windows (winget)
```powershell
winget install ngrok.ngrok
```

#### Windows (Chocolatey)
```powershell
choco install ngrok
```

### Configurar Authtoken (Primera vez)

1. Regístrate en https://ngrok.com
2. Copia tu authtoken
3. Configura:
```bash
ngrok config add-authtoken <TU_TOKEN>
```

### Uso

Con los servidores corriendo:
```bash
ngrok http 5000
```

Comparte la URL pública generada (ej: `https://abc-123.ngrok-free.app`)

## 🔍 Servicios gRPC Disponibles

### `CreateTodo`
Crea una nueva tarea.

**Request:**
```protobuf
CreateTodoRequest {
  string title = 1;
}
```

**Response:**
```protobuf
Todo {
  string id = 1;
  string title = 2;
  bool completed = 3;
}
```

### `ListTodos`
Lista todas las tareas.

**Request:**
```protobuf
Empty {}
```

**Response:**
```protobuf
TodoList {
  repeated Todo todos = 1;
}
```

### `ToggleComplete`
Alterna el estado de una tarea.

**Request:**
```protobuf
TodoIdRequest {
  string id = 1;
}
```

**Response:**
```protobuf
Todo {
  string id = 1;
  string title = 2;
  bool completed = 3;
}
```

### `DeleteTodo`
Elimina una tarea.

**Request:**
```protobuf
TodoIdRequest {
  string id = 1;
}
```

**Response:**
```protobuf
Empty {}
```

## 🐛 Troubleshooting

### Error: "Cannot import grpc"

**Causa:** El intérprete de VS Code no está usando el venv.

**Solución:**
1. Presiona `Cmd+Shift+P` (Mac) o `Ctrl+Shift+P` (Windows)
2. Busca: "Python: Select Interpreter"
3. Selecciona: `./venv/bin/python` o `Python 3.x.x (venv)`

### Error: "Connection refused" al iniciar Flask

**Causa:** El servidor gRPC no está corriendo.

**Solución:**
1. Inicia primero `server.py`
2. Espera a ver: "Servidor gRPC corriendo en http://localhost:50051"
3. Luego inicia `app.py`

### Puerto 50051 o 5000 ocupado

**Mac/Linux:**
```bash
# Ver qué proceso usa el puerto
lsof -i :50051
lsof -i :5000

# Matar proceso
kill -9 <PID>
```

**Windows (PowerShell):**
```powershell
# Ver qué proceso usa el puerto
netstat -ano | findstr :50051
netstat -ano | findstr :5000

# Matar proceso
taskkill /PID <PID> /F
```

### Error: "ModuleNotFoundError"

**Causa:** Dependencias no instaladas o venv no activado.

**Solución:**
```bash
# Asegúrate de estar en el venv
source venv/bin/activate  # Mac/Linux
.\venv\Scripts\Activate.ps1  # Windows

# Reinstala dependencias
pip install -r requirements.txt
```

### Cambios en frontend no se reflejan

**Solución:** Hard reload en el navegador
- Windows: `Ctrl + F5`
- Mac: `Cmd + Shift + R`

### Error al ejecutar run.sh: "Permission denied"

**Solución:**
```bash
chmod +x run.sh
```

### Error PowerShell: "cannot be loaded because running scripts is disabled"

**Solución:**
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## 🔄 Regenerar Archivos Protocol Buffers

Si modificas `todo.proto`, debes regenerar los archivos Python:

```bash
# Activar venv primero
source venv/bin/activate  # Mac/Linux
.\venv\Scripts\Activate.ps1  # Windows

# Regenerar
python -m grpc_tools.protoc \
  -I. \
  --python_out=. \
  --grpc_python_out=. \
  todo.proto
```

Esto actualizará:
- `todo_pb2.py`
- `todo_pb2_grpc.py`

## 📚 Dependencias del Proyecto

```
blinker==1.9.0         # Flask signaling
click==8.3.1           # Command line interface
colorama==0.4.6        # Colored terminal output
Flask==3.1.3           # Web framework
grpcio==1.78.0         # gRPC framework
grpcio-tools==1.78.0   # gRPC code generation
itsdangerous==2.2.0    # Security utilities
Jinja2==3.1.6          # Template engine
MarkupSafe==3.0.3      # String escaping
protobuf==6.33.5       # Protocol Buffers
typing_extensions==4.15.0  # Type hints
Werkzeug==3.1.6        # WSGI utilities
```

## 🎯 Flujo de Trabajo Recomendado

### Desarrollo Local

1. **Iniciar servidores con script:**
   ```bash
   ./run.sh           # Mac/Linux
   .\run.ps1          # Windows
   ```

2. **Abrir navegador:**
   http://localhost:5000

3. **Hacer cambios en el código**

4. **Reiniciar servidores:**
   - Presiona `Ctrl+C` en la terminal
   - Ejecuta nuevamente `./run.sh` o `.\run.ps1`

### Desarrollo con Acceso Remoto

1. **Iniciar servidores con ngrok:**
   ```bash
   ./run.sh           # Responde 's' cuando pregunte por ngrok
   ```

2. **Copiar URL pública de ngrok:**
   ```
   https://abc-123-def.ngrok-free.app
   ```

3. **Compartir URL** para pruebas externas

4. **Detener:** `Ctrl+C`

## 📝 Notas Adicionales

- Las tareas se almacenan **en memoria**, se pierden al reiniciar el servidor
- Para persistencia, considera agregar una base de datos (SQLite, PostgreSQL, etc.)
- El servidor gRPC usa **protocolos inseguros** (insecure_channel) para desarrollo local
- Para producción, usa **TLS/SSL** con certificados

## 🤝 Contribuir

1. Fork del repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m 'Agrega nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

---

**Desarrollado con ❤️ usando gRPC, Flask y Protocol Buffers**
