# Neural Chaos Forum - Push to Render (GitHub)

Write-Host "`n[RENDER SYNC] Push Changes to GitHub" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan

# Check if remote is configured
$remotes = (git remote)
if ($remotes -contains "origin") {
    Write-Host "[OK] GitHub remote already configured" -ForegroundColor Green
    Write-Host "     Remote: $(git remote get-url origin)" -ForegroundColor White
} else {
    Write-Host "[SETUP] Add GitHub Remote" -ForegroundColor Yellow
    $githubUrl = Read-Host "`nEnter your GitHub repo URL (e.g., https://github.com/user/neural-chaos-forum.git)"
    
    if ($githubUrl) {
        git remote add origin $githubUrl
        Write-Host "[OK] Remote added" -ForegroundColor Green
    } else {
        Write-Host "[SKIP] No GitHub configured - will need to set up manually" -ForegroundColor Yellow
    }
}

# Push to GitHub
Write-Host "`n[PUSH] Sending changes to GitHub..." -ForegroundColor Yellow
git push -u origin main 2>&1 | Select-Object -First 20

Write-Host "`n" + "=" * 70 -ForegroundColor Cyan
Write-Host "[RENDER] Auto-Deploy" -ForegroundColor Green
Write-Host "  Render will detect the push and redeploy automatically" -ForegroundColor White
Write-Host "  Check deployment progress:" -ForegroundColor White
Write-Host "  https://dashboard.render.com" -ForegroundColor Cyan

Write-Host "`n[TEST] After deployment completes:" -ForegroundColor Yellow
Write-Host "  Homepage:  https://neural-chaos-api.onrender.com" -ForegroundColor Cyan 
Write-Host "  Admin:     https://neural-chaos-api.onrender.com/admin.html" -ForegroundColor Cyan
Write-Host "  API:       https://neural-chaos-api.onrender.com/api/health" -ForegroundColor Cyan

Write-Host "`n"
