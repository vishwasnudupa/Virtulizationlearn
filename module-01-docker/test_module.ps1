# Test Script for Module 1
Write-Host "Testing Module 1: Docker & Compose..." -ForegroundColor Cyan

# Check if containers are running
$containers = docker-compose ps -q
if (-not $containers) {
    Write-Error "No containers running! Did you run 'docker-compose up -d'?"
    exit 1
}
Write-Host "[-] Containers are up." -ForegroundColor Green

# Test the API
Write-Host "[-] Sending test log to Collector..."
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/logs" -Method Post -ContentType "application/json" -Body '{"service_name": "test-script", "level": "INFO", "message": "Automated test"}'
    if ($response.status -eq "queued") {
        Write-Host "[+] API Success: Log queued." -ForegroundColor Green
    } else {
        Write-Error "API returned unexpected status: $($response.status)"
    }
} catch {
    Write-Error "Failed to connect to Collector: $_"
}

# Check Redis
Write-Host "[-] Checking Redis queue length..."
$redisOutput = docker-compose exec -T redis-queue redis-cli llen logs_queue
if ($redisOutput -match "\d+") {
    Write-Host "[+] Redis Queue Length: $redisOutput" -ForegroundColor Green
} else {
    Write-Error "Failed to check Redis."
}
