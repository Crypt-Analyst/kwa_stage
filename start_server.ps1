# PowerShell script to clear database environment variables and start Django server
# This ensures that the .env file takes precedence

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   Boda Boda Welfare System - Server Startup" -ForegroundColor Cyan  
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Clearing conflicting environment variables..." -ForegroundColor Yellow

# Clear environment variables for this session
$env:DB_HOST = $null
$env:DB_NAME = $null  
$env:DB_USER = $null
$env:DB_PASSWORD = $null
$env:DB_PORT = $null

Write-Host "✅ Environment variables cleared." -ForegroundColor Green

# Test database connection
Write-Host ""
Write-Host "Testing database connection..." -ForegroundColor Yellow
try {
    python test_db_connection.py
    if ($LASTEXITCODE -ne 0) {
        throw "Database connection test failed"
    }
    Write-Host "✅ Database connection test passed." -ForegroundColor Green
} catch {
    Write-Host "❌ Database connection test failed: $_" -ForegroundColor Red
    Write-Host "Please check your .env file and credentials." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Start Django development server
Write-Host ""
Write-Host "Starting Django development server..." -ForegroundColor Yellow
Write-Host "🌐 Server will be available at: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "⏹️  Press Ctrl+C to stop the server" -ForegroundColor Cyan
Write-Host ""

python start_server.py
