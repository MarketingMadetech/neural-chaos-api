# Neural Chaos Forum - Deployment Status Checker

Write-Host "`n[DEPLOYMENT CHECK] Neural Chaos Forum" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "Git commit pushed: 4678cf7" -ForegroundColor White
Write-Host "Render auto-deploy triggered" -ForegroundColor White
Write-Host ""

Write-Host "[WAIT] Deployment typically takes 2-3 minutes..." -ForegroundColor Yellow
Write-Host "       Check status at: https://dashboard.render.com" -ForegroundColor White
Write-Host ""

$countdown = 120
Write-Host "[COUNTDOWN] Waiting $countdown seconds before testing..." -ForegroundColor Yellow

for ($i = $countdown; $i -gt 0; $i -= 10) {
    Write-Host "  $i seconds remaining..." -ForegroundColor Gray
    Start-Sleep -Seconds 10
}

Write-Host "`n[TEST] Testing endpoints..." -ForegroundColor Cyan

$tests = @(
    @{Name="Homepage"; URL="https://neural-chaos-api.onrender.com"},
    @{Name="Admin Dashboard"; URL="https://neural-chaos-api.onrender.com/admin.html"},
    @{Name="API Health"; URL="https://neural-chaos-api.onrender.com/api/health"},
    @{Name="API Agents"; URL="https://neural-chaos-api.onrender.com/api/agents"}
)

$passed = 0
$failed = 0

foreach ($test in $tests) {
    try {
        $result = Invoke-WebRequest -Uri $test.URL -UseBasicParsing -TimeoutSec 10 -ErrorAction Stop
        if ($result.StatusCode -eq 200) {
            Write-Host "[OK] $($test.Name) - $($result.StatusCode)" -ForegroundColor Green
            $passed++
        } else {
            Write-Host "[WARN] $($test.Name) - $($result.StatusCode)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "[FAIL] $($test.Name) - $_" -ForegroundColor Red
        $failed++
    }
}

Write-Host "`n" + "=" * 70 -ForegroundColor Cyan
Write-Host "[RESULTS] Tests: $($tests.Count) | Passed: $passed | Failed: $failed" -ForegroundColor $(if ($failed -eq 0) {'Green'} else {'Yellow'})

if ($failed -eq 0) {
    Write-Host "`n[SUCCESS] Neural Chaos Forum is LIVE!" -ForegroundColor Green
    Write-Host "  Homepage: https://neural-chaos-api.onrender.com" -ForegroundColor Cyan
    Write-Host "  Admin:    https://neural-chaos-api.onrender.com/admin.html" -ForegroundColor Cyan
} else {
    Write-Host "`n[TROUBLESHOOT] Some endpoints failed" -ForegroundColor Yellow
    Write-Host "  1. Check Render logs: https://dashboard.render.com" -ForegroundColor White
    Write-Host "  2. Verify deployment completed successfully" -ForegroundColor White
    Write-Host "  3. Check build logs for errors" -ForegroundColor White
}

Write-Host ""
