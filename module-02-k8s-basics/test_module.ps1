# Test Script for Module 2
Write-Host "Testing Module 2: K8s Basics..." -ForegroundColor Cyan

# Check Pods
$pods = kubectl get pods -l app=sentinel
if (-not $pods) {
    Write-Error "No pods found with label app=sentinel"
    exit 1
}
Write-Host "[-] Pods found." -ForegroundColor Green

# Check Service
$svc = kubectl get svc collector-service
if (-not $svc) {
    Write-Error "Collector Service not found."
} else {
    Write-Host "[-] Collector Service exists." -ForegroundColor Green
}

# Check Generator Logs
Write-Host "[-] Checking Generator logs for activity..."
try {
    $logs = kubectl logs -l run=generator --tail=5
    if ($logs -match "Sent:") {
        Write-Host "[+] Generator is sending logs." -ForegroundColor Green
    } else {
        Write-Warning "Generator logs do not show 'Sent:'. It might be starting up or failing."
        Write-Host $logs
    }
} catch {
    Write-Warning "Could not get generator logs."
}
