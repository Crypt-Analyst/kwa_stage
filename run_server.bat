@echo off
echo.
echo ================================================
echo   Boda Boda Welfare System - Server Startup
echo ================================================
echo.
echo Clearing conflicting environment variables...

REM Clear database environment variables
set "DB_HOST="
set "DB_NAME="
set "DB_USER="
set "DB_PASSWORD="
set "DB_PORT="

echo ✅ Environment variables cleared.
echo.
echo Starting Django development server...
echo Server will be available at: http://127.0.0.1:8000
echo Press Ctrl+C to stop the server
echo.

python start_server.py

pause
