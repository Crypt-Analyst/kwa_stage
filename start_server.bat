@echo off
echo Clearing database environment variables...
set DB_HOST=
set DB_NAME=
set DB_USER=
set DB_PASSWORD=
set DB_PORT=

echo Testing database connection...
python manage.py shell -c "from django.db import connection; cursor = connection.cursor(); cursor.execute('SELECT 1'); print('Database connection successful!')"

if %ERRORLEVEL% NEQ 0 (
    echo Database connection failed!
    pause
    exit /b 1
)

echo Starting Django development server...
echo Server will be available at: http://127.0.0.1:8000
echo Press Ctrl+C to stop the server

python manage.py runserver
