# Test Script for Module 3
Write-Host "Testing Module 3: Config & State..." -ForegroundColor Cyan

# Check StatefulSet
$sts = kubectl get statefulset redis
if (-not $sts) {
    Write-Error "Redis StatefulSet not found."
    exit 1
}
Write-Host "[-] Redis StatefulSet exists." -ForegroundColor Green

# Check ConfigMap
$cm = kubectl get cm analyzer-config
if (-not $cm) {
    Write-Error "ConfigMap analyzer-config not found."
} else {
    Write-Host "[-] ConfigMap exists." -ForegroundColor Green
}

# Check Persistence (PVC)
$pvc = kubectl get pvc redis-data-redis-0
if (-not $pvc) {
    Write-Error "PVC redis-data-redis-0 not found."
} else {
    Write-Host "[-] PVC exists." -ForegroundColor Green
}
