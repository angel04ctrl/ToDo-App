# 📋 ToDo-App

Aplicación de gestión de tareas con arquitectura cliente-servidor usando **gRPC** y **Flask**.

## 🚀 Inicio Rápido

### Mac/Linux
```bash
./run.sh
```

### Windows
```powershell
powershell -ExecutionPolicy Bypass -File run.ps1
```

Luego abre http://localhost:5000 en tu navegador.

## 🏗️ Arquitectura

```
Browser → Flask (puerto 5000) → gRPC Server (puerto 50051)
```

- **Frontend:** Interfaz web con HTML/CSS/JS
- **Flask Server:** API REST que actúa como cliente gRPC
- **gRPC Server:** Backend con lógica de negocio

## 📦 Instalación Manual

```bash
# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# .\venv\Scripts\Activate.ps1  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python3 server.py  # Terminal 1
python3 app.py     # Terminal 2
```

## 📚 Documentación Completa

Para guía detallada de instalación, troubleshooting, API y más, consulta [SETUP.md](SETUP.md).

## ✨ Características

- ✅ Crear tareas
- ✅ Marcar como completadas
- ✅ Eliminar tareas
- ✅ Interfaz responsive
- ✅ Comunicación gRPC
- ✅ API REST

## 🛠️ Tecnologías

- Python 3.9+
- gRPC & Protocol Buffers
- Flask
- HTML/CSS/JavaScript

## 📄 Licencia

MIT