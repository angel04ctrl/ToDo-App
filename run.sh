#!/bin/bash

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE} Iniciando ToDo-App...${NC}"
echo ""

# Validar que estamos en la carpeta raíz del proyecto
if [ ! -f "server.py" ] || [ ! -f "app.py" ]; then
    echo -e "${RED}  Por favor ejecuta este script desde la raíz del proyecto${NC}"
    exit 1
fi

# Validar que existe el venv
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}  No se encontró el entorno virtual. Creándolo...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    echo -e "${GREEN} Entorno virtual creado e instalado${NC}"
else
    source venv/bin/activate
    echo -e "${GREEN} Entorno virtual activado${NC}"
fi

# Función para limpiar procesos al salir
cleanup() {
    echo -e "${YELLOW}\n⏹️  Deteniendo servidores...${NC}"
    kill $GRPC_PID $FLASK_PID 2>/dev/null
    echo -e "${GREEN} Servidores detenidos${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Terminal 1: gRPC Server
echo -e "${GREEN}[1/3] Levantando gRPC Server en puerto 50051${NC}"
python3 server.py &
GRPC_PID=$!
echo -e "${BLUE}gRPC PID: $GRPC_PID${NC}"

# Esperar a que gRPC esté listo
sleep 3

# Terminal 2: Flask Server
echo -e "${GREEN}[2/3] Levantando Flask Server en puerto 5000${NC}"
python3 app.py &
FLASK_PID=$!
echo -e "${BLUE}Flask PID: $FLASK_PID${NC}"

# Esperar a que Flask esté listo
sleep 2

# Terminal 3: ngrok (opcional)
echo ""
echo -e "${GREEN}[3/3] ¿Quieres levantar ngrok para acceso remoto? (s/n)${NC}"
read -r response
if [[ "$response" =~ ^[Ss]$ ]]; then
    echo -e "${BLUE}Levantando ngrok en puerto 5000...${NC}"
    ngrok http 5000
else
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN} Servidores activos:${NC}"
    echo -e "   ${BLUE} gRPC Server:${NC} http://localhost:50051"
    echo -e "   ${BLUE} Web App:${NC} http://localhost:5000"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${YELLOW} Presiona Ctrl+C para detener los servidores${NC}"
    echo ""
    wait
fi
