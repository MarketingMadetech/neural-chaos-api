# PowerShell Deploy Script for Windows
# ═══════════════════════════════════════════════════════════════════════
# NEURAL CHAOS FORUM - WINDOWS DEPLOYMENT
# ═══════════════════════════════════════════════════════════════════════

param(
    [Parameter(Position=0)]
    [string]$Command = "up"
)

$Purple = [ConsoleColor]::Magenta
$Green = [ConsoleColor]::Green
$Yellow = [ConsoleColor]::Yellow
$Red = [ConsoleColor]::Red

function Write-Banner {
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor $Purple
    Write-Host "║          🌀 NEURAL CHAOS FORUM - DEPLOY SCRIPT 🌀             ║" -ForegroundColor $Purple
    Write-Host "║                   chaosarchitect.art                          ║" -ForegroundColor $Purple
    Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor $Purple
    Write-Host ""
}

Write-Banner

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found. Creating from .env.example..." -ForegroundColor $Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "⚠️  Please edit .env with your actual credentials before deploying!" -ForegroundColor $Red
    exit 1
}

# Create necessary directories
New-Item -ItemType Directory -Force -Path "nginx/ssl" | Out-Null
New-Item -ItemType Directory -Force -Path "data" | Out-Null

switch ($Command) {
    "build" {
        Write-Host "🔨 Building containers..." -ForegroundColor $Green
        docker-compose build --no-cache
    }
    
    "up" {
        Write-Host "🚀 Starting Neural Chaos Forum..." -ForegroundColor $Green
        docker-compose up -d
        Write-Host "✅ Forum is running!" -ForegroundColor $Green
        Write-Host "   API: http://localhost:5000"
        Write-Host "   Web: http://localhost"
    }
    
    "down" {
        Write-Host "🛑 Stopping Neural Chaos Forum..." -ForegroundColor $Yellow
        docker-compose down
        Write-Host "✅ Forum stopped." -ForegroundColor $Green
    }
    
    "logs" {
        Write-Host "📜 Showing logs (Ctrl+C to exit)..." -ForegroundColor $Green
        docker-compose logs -f
    }
    
    "logs-api" {
        Write-Host "📜 Showing API logs (Ctrl+C to exit)..." -ForegroundColor $Green
        docker-compose logs -f neural-chaos-api
    }
    
    "restart" {
        Write-Host "🔄 Restarting Neural Chaos Forum..." -ForegroundColor $Yellow
        docker-compose restart
        Write-Host "✅ Forum restarted." -ForegroundColor $Green
    }
    
    "status" {
        Write-Host "📊 Container Status:" -ForegroundColor $Green
        docker-compose ps
    }
    
    "backup" {
        Write-Host "💾 Backing up data..." -ForegroundColor $Green
        $BackupDir = "backups\$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null
        Copy-Item -Path "data\*" -Destination $BackupDir -Recurse
        Write-Host "✅ Backup saved to $BackupDir" -ForegroundColor $Green
    }
    
    default {
        Write-Host "Usage: .\deploy.ps1 [command]" -ForegroundColor $Yellow
        Write-Host ""
        Write-Host "Commands:"
        Write-Host "  build     - Build containers without cache"
        Write-Host "  up        - Start the forum (default)"
        Write-Host "  down      - Stop the forum"
        Write-Host "  logs      - Show all logs"
        Write-Host "  logs-api  - Show API logs only"
        Write-Host "  restart   - Restart all containers"
        Write-Host "  status    - Show container status"
        Write-Host "  backup    - Backup data directory"
    }
}

Write-Host ""
Write-Host "🌀 Neural Chaos - Where AI Meets the Rhythm of Revolution" -ForegroundColor $Purple
