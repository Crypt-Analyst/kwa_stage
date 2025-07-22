#!/usr/bin/env python
"""
Setup script to create default organization and update existing data
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bodaboda_welfare.settings')
django.setup()

from django.contrib.auth.models import User
from stages.models import Organization, Stage

def setup_default_data():
    """Create default organization and assign existing stages"""
    
    # Create default admin user if none exists
    admin_user, user_created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@default.com',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    
    if user_created:
        admin_user.set_password('admin123')  # Change this in production!
        admin_user.save()
        print(f"Created default admin user: {admin_user.username}")
    else:
        print(f"Default admin user already exists: {admin_user.username}")
    
    # Create default organization
    default_org, created = Organization.objects.get_or_create(
        name='Default SACCO',
        defaults={
            'organization_type': 'sacco',
            'registration_number': 'DEFAULT001',
            'description': 'Default organization for existing stages',
            'email': 'admin@default.com',
            'phone_number': '+254700000000',
            'county': 'Nairobi',
            'sub_county': 'Westlands',
            'town': 'Nairobi',
            'address': 'Default Address',
            'admin_user': admin_user,
            'is_active': True,
        }
    )
    
    if created:
        print(f"Created default organization: {default_org.name}")
    else:
        print(f"Default organization already exists: {default_org.name}")
    
    # Update existing stages without organization
    stages_updated = Stage.objects.filter(organization__isnull=True).update(
        organization=default_org
    )
    
    print(f"Updated {stages_updated} stages with default organization")
    
    # Show summary
    print(f"\nSummary:")
    print(f"- Organizations: {Organization.objects.count()}")
    print(f"- Stages: {Stage.objects.count()}")
    
    return default_org

if __name__ == '__main__':
    setup_default_data()
