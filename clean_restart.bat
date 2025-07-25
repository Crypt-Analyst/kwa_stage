@echo off
echo =========================================
echo  Clean Django Restart with Fresh ENV
echo =========================================

REM Kill any existing Python processes
echo Stopping any running Django servers...
taskkill /f /im python.exe 2>nul

REM Clear all environment variables that might conflict
echo Clearing environment variables...
set CLOUDFLARE_TURNSTILE_SITE_KEY=
set CLOUDFLARE_TURNSTILE_SECRET_KEY=
set DB_NAME=
set DB_USER=
set DB_PASSWORD=
set DB_HOST=
set DB_PORT=

REM Wait a moment
timeout /t 2 /nobreak >nul

REM Start Django with fresh environment
echo Starting Django server with fresh environment...
echo Server will be available at: http://127.0.0.1:8000
echo.
python manage.py runserver

pause
