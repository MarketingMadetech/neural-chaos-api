# Neural Chaos Forum - Deploy to Render (Updated Frontend Routes)

Write-Host "`n[RENDER REDEPLOY] Deploy Updated Frontend Routes" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan

# Option 1: If you have GitHub connected to Render
Write-Host "`n[Option 1] GitHub Push (Recommended)" -ForegroundColor Yellow
Write-Host "If GitHub is connected to Render:"
Write-Host "  git add ." -ForegroundColor White
Write-Host "  git commit -m 'fix: Add static routes for HTML'" -ForegroundColor White  
Write-Host "  git push origin main" -ForegroundColor White
Write-Host "`nRender auto-deploys in 1-2 minutes." -ForegroundColor Green

# Option 2: Render Dashboard Manual Deploy
Write-Host "`n[Option 2] Manual Deploy via Dashboard" -ForegroundColor Yellow
Write-Host "  1. Visit: https://dashboard.render.com" -ForegroundColor White
Write-Host "  2. Select: neural-chaos-api" -ForegroundColor White
Write-Host "  3. Click: Manual Deploy --> Deploy latest commit" -ForegroundColor White
Write-Host "  4. Wait 2-3 minutes for deployment" -ForegroundColor White

# Option 3: Status Check
Write-Host "`n[Option 3] Verify Deployment" -ForegroundColor Yellow
Write-Host "After deploying, test these URLs:" -ForegroundColor White
Write-Host "  Home: https://neural-chaos-api.onrender.com" -ForegroundColor Cyan
Write-Host "  Admin: https://neural-chaos-api.onrender.com/admin.html" -ForegroundColor Cyan
Write-Host "  API: https://neural-chaos-api.onrender.com/api/health" -ForegroundColor Cyan

Write-Host "`n" + "=" * 70 -ForegroundColor Cyan
Write-Host "[CHANGE SUMMARY]" -ForegroundColor Green  
Write-Host "  GET /  --> Serves index.html (homepage)" -ForegroundColor White
Write-Host "  GET /admin.html --> Serves admin.html (dashboard)" -ForegroundColor White

Write-Host "`n[LOCAL TEST] Already working:" -ForegroundColor Green
Write-Host "  http://localhost:5000  --> OK (29KB of HTML)" -ForegroundColor White

Write-Host "`n[NEXT STEP] Deploy to production now!" -ForegroundColor Yellow
Write-Host ""
