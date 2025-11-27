# Test Script for Module 1
Write-Host "Testing Module 1: Docker & Compose..." -ForegroundColor Cyan

# 1. Check for Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "CRITICAL: Docker is not installed or not in your PATH."
    Write-Host "Please install Docker Desktop and restart your terminal." -ForegroundColor Yellow
    exit 1
}

# 2. Detect Compose Command
$composeCmd = "docker-compose"
if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    # Try 'docker compose' (V2)
    $dockerVersion = docker compose version 2>&1
    if ($dockerVersion -match "Docker Compose") {
        $composeCmd = "docker compose"
    } else {
        Write-Error "CRITICAL: Neither 'docker-compose' nor 'docker compose' found."
        exit 1
    }
}
Write-Host "[-] Using Compose command: '$composeCmd'" -ForegroundColor Gray

# 3. Check if containers are running
# We use Invoke-Expression because $composeCmd might contain a space
$containers = Invoke-Expression "$composeCmd ps -q"
if (-not $containers) {
    Write-Error "No containers running! Did you run '$composeCmd up -d'?"
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
$redisOutput = Invoke-Expression "$composeCmd exec -T redis-queue redis-cli llen logs_queue"
if ($redisOutput -match "\d+") {
    Write-Host "[+] Redis Queue Length: $redisOutput" -ForegroundColor Green
} else {
    Write-Error "Failed to check Redis."
}
