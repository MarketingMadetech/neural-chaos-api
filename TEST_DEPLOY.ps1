# Neural Chaos Forum - Final Test

Write-Host "`n[FIX APLICADO] O que foi corrigido:" -ForegroundColor Cyan
Write-Host "=" * 70

Write-Host "`nProblema: gunicorn --chdir api server:app (ERRADO)"
Write-Host "Solucao:  gunicorn server:app (CORRETO)"
Write-Host ""
Write-Host "Motivo: Arquivos ja estao em /app/, nao precisava chdir"

Write-Host "`n[DEPLOY] Commit 633f3f5 enviado" -ForegroundColor Yellow
Write-Host "  Render fazendo rebuild..."
Write-Host "  Aguardando 120 segundos..."
Write-Host ""

for ($i = 120; $i -gt 0; $i -= 20) {
    Write-Host "  $i segundos..." -ForegroundColor Gray
    Start-Sleep -Seconds 20
}

Write-Host "`n[TESTE] Verificando endpoints..." -ForegroundColor Cyan
Write-Host ""

$urls = @{
    "Homepage" = "https://neural-chaos-api.onrender.com"
    "Admin" = "https://neural-chaos-api.onrender.com/admin.html"
    "Health" = "https://neural-chaos-api.onrender.com/api/health"
}

$ok = 0
foreach ($name in $urls.Keys) {
    try {
        $r = Invoke-WebRequest -Uri $urls[$name] -UseBasicParsing -TimeoutSec 15 -ErrorAction Stop
        Write-Host "[OK] $name - $($r.StatusCode)" -ForegroundColor Green
        $ok++
    } catch {
        Write-Host "[FAIL] $name - $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n" + "=" * 70
if ($ok -eq 3) {
    Write-Host "[SUCCESS] Tudo funcionando!" -ForegroundColor Green
    Write-Host ""
    Write-Host "URLs:"
    Write-Host "  https://neural-chaos-api.onrender.com"
    Write-Host "  https://neural-chaos-api.onrender.com/admin.html"
    Write-Host ""
} else {
    Write-Host "[STATUS] $ok/3 funcionando" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Aguarde mais 1-2 minutos se ainda houver erros."
}
Write-Host ""
