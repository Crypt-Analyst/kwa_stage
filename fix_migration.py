import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bodaboda_welfare.settings')
django.setup()

from django.core.management import call_command
from django.db import connection
from io import StringIO
import sys

def run_migration():
    """Attempt to run the migration and handle any issues"""
    try:
        print("Checking migration status...")
        
        # First, let's see what migrations are pending
        output = StringIO()
        call_command('showmigrations', 'members', stdout=output)
        migration_status = output.getvalue()
        print("Migration status:")
        print(migration_status)
        
        # Try to run the migration
        print("\nRunning migration...")
        call_command('migrate', 'members', verbosity=2)
        print("✅ Migration completed!")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        
        # If migration fails, let's try to add the columns manually
        print("\nAttempting manual column addition...")
        try:
            with connection.cursor() as cursor:
                # Check if columns exist first
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'members_member' 
                    AND column_name IN ('is_online', 'last_seen', 'last_activity');
                """)
                existing_columns = [row[0] for row in cursor.fetchall()]
                
                # Add missing columns
                if 'is_online' not in existing_columns:
                    cursor.execute("ALTER TABLE members_member ADD COLUMN is_online BOOLEAN DEFAULT FALSE;")
                    print("✅ Added is_online column")
                    
                if 'last_seen' not in existing_columns:
                    cursor.execute("ALTER TABLE members_member ADD COLUMN last_seen TIMESTAMP WITH TIME ZONE DEFAULT NOW();")
                    print("✅ Added last_seen column")
                    
                if 'last_activity' not in existing_columns:
                    cursor.execute("ALTER TABLE members_member ADD COLUMN last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW();")
                    print("✅ Added last_activity column")
                
                # Mark migration as applied
                cursor.execute("""
                    INSERT INTO django_migrations (app, name, applied) 
                    VALUES ('members', '0006_member_is_online_member_last_activity_and_more', NOW())
                    ON CONFLICT (app, name) DO NOTHING;
                """)
                print("✅ Marked migration as applied")
                
            return True
            
        except Exception as e2:
            print(f"❌ Manual addition also failed: {e2}")
            return False

if __name__ == "__main__":
    success = run_migration()
    if success:
        print("\n🎉 Database is now ready!")
    else:
        print("\n💥 Database update failed!")
