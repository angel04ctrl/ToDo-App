$GREEN = "Green"
$BLUE = "Cyan"
$YELLOW = "Yellow"
$RED = "Red"

Write-Host "🚀 Iniciando ToDo-App..." -ForegroundColor $BLUE
Write-Host ""

# Validar que estamos en la carpeta raíz
if (-not (Test-Path "server.py") -or -not (Test-Path "app.py")) {
    Write-Host "  Por favor ejecuta este script desde la raíz del proyecto" -ForegroundColor $RED
    exit 1
}

# Validar que existe el venv
if (-not (Test-Path "venv")) {
    Write-Host " No se encontró el entorno virtual. Creándolo..." -ForegroundColor $YELLOW
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    Write-Host " Entorno virtual creado e instalado" -ForegroundColor $GREEN
} else {
    .\venv\Scripts\Activate.ps1
    Write-Host " Entorno virtual activado" -ForegroundColor $GREEN
}

# Terminal 1: gRPC Server
Write-Host "[1/3] Levantando gRPC Server en puerto 50051" -ForegroundColor $GREEN
$grpcProcess = Start-Process python -ArgumentList "server.py" -PassThru -WindowStyle Hidden
Write-Host "gRPC PID: $($grpcProcess.Id)" -ForegroundColor $BLUE
Start-Sleep -Seconds 3

# Terminal 2: Flask Server
Write-Host "[2/3] Levantando Flask Server en puerto 5000" -ForegroundColor $GREEN
$flaskProcess = Start-Process python -ArgumentList "app.py" -PassThru -WindowStyle Hidden
Write-Host "Flask PID: $($flaskProcess.Id)" -ForegroundColor $BLUE
Start-Sleep -Seconds 2

# Terminal 3: ngrok (opcional)
Write-Host ""
Write-Host "[3/3] ¿Quieres levantar ngrok para acceso remoto? (s/n)" -ForegroundColor $GREEN
$response = Read-Host

if ($response -eq "s" -or $response -eq "S") {
    Write-Host "Levantando ngrok en puerto 5000..." -ForegroundColor $BLUE
    & ngrok http 5000
    
    # Limpiar procesos al cerrar ngrok
    Stop-Process -Id $grpcProcess.Id -Force
    Stop-Process -Id $flaskProcess.Id -Force
} else {
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $BLUE
    Write-Host " Servidores activos:" -ForegroundColor $GREEN
    Write-Host "    gRPC Server: http://localhost:50051" -ForegroundColor $BLUE
    Write-Host "    Web App: http://localhost:5000" -ForegroundColor $BLUE
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $BLUE
    Write-Host ""
    Write-Host " Presiona Ctrl+C para detener los servidores" -ForegroundColor $YELLOW
    Write-Host ""
    
    # Esperar indefinidamente hasta que el usuario presione Ctrl+C
    try {
        while ($true) {
            Start-Sleep -Seconds 1
        }
    } finally {
        # Limpiar procesos al salir
        Write-Host ""
        Write-Host "⏹  Deteniendo servidores..." -ForegroundColor $YELLOW
        Stop-Process -Id $grpcProcess.Id -Force -ErrorAction SilentlyContinue
        Stop-Process -Id $flaskProcess.Id -Force -ErrorAction SilentlyContinue
        Write-Host " Servidores detenidos" -ForegroundColor $GREEN
    }
}
