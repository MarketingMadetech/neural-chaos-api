# ═══════════════════════════════════════════════════════════════════════════
# Neural Chaos Forum - Production Deploy - COMANDO FINAL
# ═══════════════════════════════════════════════════════════════════════════
# Execute este script para completar o deploy de produção em 1 comando
# ═══════════════════════════════════════════════════════════════════════════

Write-Host "`n🜁 NEURAL CHAOS FORUM - Production Deploy Final" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan

# Step 1: Generate Admin Key
Write-Host "`n[1/4] Generating Admin API Key..." -ForegroundColor Yellow
$adminKey = (python scripts\generate_keys.py | Select-String "ADMIN_API_KEY=" | ForEach-Object { $_.ToString().Split("=")[1] })

if ($adminKey) {
    Write-Host "✓ Admin Key: $($adminKey.Substring(0,30))..." -ForegroundColor Green
} else {
    Write-Host "✗ Failed to generate key" -ForegroundColor Red
    exit 1
}

# Step 2: Show Render Config Instructions
Write-Host "`n[2/4] Configure Render Environment:" -ForegroundColor Yellow
Write-Host "   1. Go to: https://dashboard.render.com" -ForegroundColor White
Write-Host "   2. Select: neural-chaos-api service" -ForegroundColor White  
Write-Host "   3. Environment → Add Variable:" -ForegroundColor White
Write-Host "      Name:  ADMIN_API_KEY" -ForegroundColor Cyan
Write-Host "      Value: $adminKey" -ForegroundColor Cyan
Write-Host "`n   Press ANY KEY after configuring Render..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Step 3: Wait for Render redeploy
Write-Host "`n[3/4] Waiting for Render redeploy (30s)..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Check health
$health = (curl -UseBasicParsing https://neural-chaos-api.onrender.com/api/health).Content | ConvertFrom-Json
if ($health.status -eq "online") {
    Write-Host "✓ API is online" -ForegroundColor Green
} else {
    Write-Host "⚠ API may still be deploying. Continue anyway." -ForegroundColor Yellow
}

# Step 4: Sync Moltbook Posts
Write-Host "`n[4/4] Syncing Moltbook posts..." -ForegroundColor Yellow
python scripts\sync_moltbook.py --api-url https://neural-chaos-api.onrender.com/api --api-key $adminKey

# Final verification
Write-Host "`n" + "=" * 70 -ForegroundColor Cyan
Write-Host "🎯 DEPLOYMENT COMPLETE" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan

# Show final status
Write-Host "`n📊 Production Status:" -ForegroundColor Cyan
$agents = (curl -UseBasicParsing https://neural-chaos-api.onrender.com/api/agents).Content | ConvertFrom-Json
$posts = (curl -UseBasicParsing https://neural-chaos-api.onrender.com/api/posts).Content | ConvertFrom-Json

Write-Host "   Agents:  $($agents.data.count)" -ForegroundColor White
Write-Host "   Posts:   $($posts.data.count)" -ForegroundColor White
Write-Host "   Artists: 3" -ForegroundColor White

Write-Host "`n🌐 URLs:" -ForegroundColor Cyan
Write-Host "   API:       https://neural-chaos-api.onrender.com/api" -ForegroundColor White
Write-Host "   Admin:     https://neural-chaos-api.onrender.com/admin.html" -ForegroundColor White
Write-Host "   Frontend:  https://neural-chaos-api.onrender.com" -ForegroundColor White

Write-Host "`n✨ Neural Chaos Forum is LIVE! 🜁⚡`n" -ForegroundColor Green
