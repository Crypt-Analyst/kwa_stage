#!/usr/bin/env python3

import os
import sys
import django
from django.db import connection

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bodaboda_welfare.settings')
django.setup()

def check_table_schema():
    """Check the current schema of social_groupchat table"""
    print("=" * 60)
    print("🔍 CHECKING SOCIAL_GROUPCHAT TABLE SCHEMA")
    print("=" * 60)
    
    with connection.cursor() as cursor:
        # Check if table exists
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = 'social_groupchat' 
            AND table_schema = 'public'
        """)
        
        table_exists = cursor.fetchone()
        print(f"📋 Table 'social_groupchat' exists: {'✅' if table_exists else '❌'}")
        
        if table_exists:
            # Get table columns
            cursor.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'social_groupchat'
                AND table_schema = 'public'
                ORDER BY ordinal_position
            """)
            
            columns = cursor.fetchall()
            print(f"\n📊 Current columns in social_groupchat:")
            
            has_created_by = False
            for column_name, data_type, is_nullable in columns:
                nullable = "NULL" if is_nullable == "YES" else "NOT NULL"
                print(f"   - {column_name}: {data_type} ({nullable})")
                if column_name == 'created_by_id':
                    has_created_by = True
            
            print(f"\n🎯 'created_by_id' column exists: {'✅' if has_created_by else '❌'}")
            
            if not has_created_by:
                print(f"\n🔧 FIXING: Adding created_by_id column...")
                try:
                    cursor.execute("""
                        ALTER TABLE social_groupchat 
                        ADD COLUMN created_by_id INTEGER NULL 
                        REFERENCES members_member(id) ON DELETE CASCADE
                    """)
                    print(f"   ✅ Column added successfully!")
                    
                    # Also add the foreign key constraint if needed
                    cursor.execute("""
                        CREATE INDEX IF NOT EXISTS social_groupchat_created_by_id_idx 
                        ON social_groupchat(created_by_id)
                    """)
                    print(f"   ✅ Index created successfully!")
                    
                except Exception as e:
                    print(f"   ❌ Error adding column: {e}")
            
        # Check migration status
        print(f"\n📋 Migration Status:")
        cursor.execute("""
            SELECT app, name, applied 
            FROM django_migrations 
            WHERE app = 'social'
            ORDER BY id
        """)
        
        migrations = cursor.fetchall()
        for app, name, applied in migrations:
            status = "✅ Applied" if applied else "❌ Not Applied"
            print(f"   - {name}: {status}")

if __name__ == '__main__':
    check_table_schema()
