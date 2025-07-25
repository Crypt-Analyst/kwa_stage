#!/usr/bin/env python3

import os
import sys
import django
from django.db import connection, transaction

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bodaboda_welfare.settings')
django.setup()

def fix_groupchat_table():
    """Add the missing created_by_id column to social_groupchat table"""
    print("🔧 FIXING SOCIAL_GROUPCHAT TABLE")
    print("=" * 50)
    
    try:
        with connection.cursor() as cursor:
            # Check if the column already exists
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'social_groupchat' 
                AND column_name = 'created_by_id'
                AND table_schema = 'public'
            """)
            
            column_exists = cursor.fetchone()
            
            if column_exists:
                print("✅ Column 'created_by_id' already exists!")
                return True
            
            print("❌ Column 'created_by_id' missing. Adding it now...")
            
            # Add the column
            cursor.execute("""
                ALTER TABLE social_groupchat 
                ADD COLUMN created_by_id INTEGER NULL
            """)
            print("✅ Column added successfully!")
            
            # Add foreign key constraint
            cursor.execute("""
                ALTER TABLE social_groupchat 
                ADD CONSTRAINT social_groupchat_created_by_id_fk 
                FOREIGN KEY (created_by_id) 
                REFERENCES members_member(id) 
                ON DELETE CASCADE
            """)
            print("✅ Foreign key constraint added!")
            
            # Add index for performance
            cursor.execute("""
                CREATE INDEX social_groupchat_created_by_id_idx 
                ON social_groupchat(created_by_id)
            """)
            print("✅ Index created!")
            
            # Mark the migration as applied
            cursor.execute("""
                INSERT INTO django_migrations (app, name, applied) 
                VALUES ('social', '0002_add_created_by_to_groupchat', NOW())
                ON CONFLICT (app, name) DO NOTHING
            """)
            print("✅ Migration marked as applied!")
            
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    success = fix_groupchat_table()
    
    if success:
        print(f"\n🎉 GroupChat table fixed successfully!")
        print(f"   You can now access /social/chats/ without errors.")
    else:
        print(f"\n❌ Failed to fix GroupChat table.")
        print(f"   Please check the error messages above.")
