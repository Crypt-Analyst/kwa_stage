import os
import sys
import django

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bodaboda_welfare.settings')

# Setup Django
django.setup()

# Import after Django setup
from django.core.management import call_command

try:
    print("Running migrations for members app...")
    call_command('migrate', 'members')
    print("Migration completed successfully!")
    
    # Also run all pending migrations
    print("Running all pending migrations...")
    call_command('migrate')
    print("All migrations completed!")
    
except Exception as e:
    print(f"Error running migrations: {e}")
    import traceback
    traceback.print_exc()
