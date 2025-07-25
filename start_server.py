#!/usr/bin/env python
"""
Script to start Django development server with correct environment variables
This ensures the .env file takes precedence over system environment variables
"""
import os
import sys
from pathlib import Path

# Get the directory containing this script
BASE_DIR = Path(__file__).resolve().parent

# Clear any existing database environment variables
for var in ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_PORT']:
    if var in os.environ:
        del os.environ[var]
        print(f"Cleared system environment variable: {var}")

# Add the project directory to Python path
sys.path.insert(0, str(BASE_DIR))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bodaboda_welfare.settings')

# Import Django and start the server
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    print("🚀 Starting Boda Boda Welfare System...")
    print("=" * 50)
    
    django.setup()
    
    # Verify the database connection
    print("🔍 Testing database connection...")
    from django.db import connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection successful!")
        
        # Check if we have any data
        from members.models import Member
        member_count = Member.objects.count()
        print(f"📊 Found {member_count} members in database")
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n💡 Try running the batch file: start_server.bat")
        sys.exit(1)
    
    print("=" * 50)
    print("🌐 Starting Django development server...")
    print("🔗 Server will be available at: http://127.0.0.1:8000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start the development server
    execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000'])
