import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bodaboda_welfare.settings')
django.setup()

from django.db import connection

def check_table_schema():
    """Check if the is_online column exists in members_member table"""
    with connection.cursor() as cursor:
        # Get table schema
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'members_member'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        
        print("Members table schema:")
        print("-" * 60)
        for column in columns:
            print(f"{column[0]:25} | {column[1]:15} | {column[2]:10} | {str(column[3])[:15]}")
        
        # Check specifically for online status columns
        online_columns = [col for col in columns if col[0] in ['is_online', 'last_seen', 'last_activity']]
        
        if online_columns:
            print(f"\n✅ Found {len(online_columns)} online status columns:")
            for col in online_columns:
                print(f"  - {col[0]}")
        else:
            print("\n❌ Online status columns not found!")
            
        return len(online_columns) == 3

if __name__ == "__main__":
    try:
        schema_ok = check_table_schema()
        if schema_ok:
            print("\n✅ Database schema is correct!")
        else:
            print("\n❌ Database schema needs migration!")
    except Exception as e:
        print(f"Error checking schema: {e}")
        import traceback
        traceback.print_exc()
