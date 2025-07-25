# PowerShell script to run Django migrations with proper environment setup

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   Running Django Migrations" -ForegroundColor Cyan  
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Clearing conflicting environment variables..." -ForegroundColor Yellow

# Clear environment variables for this session
$env:DB_HOST = $null
$env:DB_NAME = $null  
$env:DB_USER = $null
$env:DB_PASSWORD = $null
$env:DB_PORT = $null
$env:DEBUG = $null
$env:SECRET_KEY = $null
$env:EMAIL_HOST = $null
$env:EMAIL_HOST_USER = $null
$env:EMAIL_HOST_PASSWORD = $null
$env:MPESA_CONSUMER_KEY = $null
$env:MPESA_CONSUMER_SECRET = $null
$env:MPESA_PASSKEY = $null
$env:SMS_API_KEY = $null
$env:CLOUDFLARE_TURNSTILE_SITE_KEY = $null
$env:CLOUDFLARE_TURNSTILE_SECRET_KEY = $null

Write-Host "✅ Environment variables cleared." -ForegroundColor Green

Write-Host ""
Write-Host "Running Django migrations..." -ForegroundColor Blue

# Run migrations
python manage.py migrate

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Migrations completed successfully!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "❌ Migrations failed with exit code: $LASTEXITCODE" -ForegroundColor Red
}

Write-Host ""
