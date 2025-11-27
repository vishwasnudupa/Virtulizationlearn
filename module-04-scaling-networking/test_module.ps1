# Test Script for Module 4
Write-Host "Testing Module 4: Scaling & Networking..." -ForegroundColor Cyan

# Check Ingress
$ing = kubectl get ingress sentinel-ingress
if (-not $ing) {
    Write-Error "Ingress not found."
    exit 1
}
Write-Host "[-] Ingress exists." -ForegroundColor Green

# Check HPA
$hpa = kubectl get hpa analyzer-hpa
if (-not $hpa) {
    Write-Error "HPA not found."
} else {
    Write-Host "[-] HPA exists." -ForegroundColor Green
}

# Check Dashboard Access (requires DNS/Hosts setup, so we check if Service exists)
$svc = kubectl get svc dashboard-service
if ($svc) {
    Write-Host "[-] Dashboard Service is active." -ForegroundColor Green
}
