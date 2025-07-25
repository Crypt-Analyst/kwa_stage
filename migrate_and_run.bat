@echo off
echo Clearing environment variables and running migrations...

set DB_HOST=
set DB_NAME=
set DB_USER=
set DB_PASSWORD=
set DB_PORT=
set DEBUG=
set SECRET_KEY=

echo Running Django migrations...
python manage.py migrate

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Migrations completed successfully!
    echo.
    echo Starting Django server...
    python manage.py runserver 127.0.0.1:8000
) else (
    echo.
    echo Migration failed!
    pause
)
