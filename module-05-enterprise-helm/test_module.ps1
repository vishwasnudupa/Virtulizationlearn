# Test Script for Module 5
Write-Host "Testing Module 5: Helm..." -ForegroundColor Cyan

# Check Helm Release
$release = helm list -q
if ($release -match "sentinel") {
    Write-Host "[-] Helm release found: $release" -ForegroundColor Green
} else {
    Write-Warning "No Helm release found with 'sentinel' in name."
}

# Check Network Policy
$netpol = kubectl get networkpolicy redis-access-policy
if ($netpol) {
    Write-Host "[-] Network Policy exists." -ForegroundColor Green
} else {
    Write-Error "Network Policy not found."
}
