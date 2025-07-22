#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the sys.path
sys.path.append('c:/Users/bilfo/Kwa Stage')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bodaboda_welfare.settings')

django.setup()

from stages.models import Stage

# Check if any stages exist
stages = Stage.objects.all()
print(f"Total stages in database: {stages.count()}")

if stages.exists():
    print("\nExisting stages:")
    for stage in stages:
        print(f"- {stage.name} ({stage.location}, {stage.county})")
else:
    print("No stages found in database!")
    print("Creating some sample stages...")
    
    # Create some sample stages
    sample_stages = [
        {
            'name': 'Westlands Stage',
            'location': 'Westlands, Nairobi',
            'county': 'nairobi',
            'description': 'Main stage in Westlands area'
        },
        {
            'name': 'Kikuyu Stage',
            'location': 'Kikuyu Town, Kiambu',
            'county': 'kiambu',
            'description': 'Central stage in Kikuyu town'
        },
        {
            'name': 'Thika Stage',
            'location': 'Thika Town, Kiambu',
            'county': 'kiambu',
            'description': 'Main stage in Thika town'
        },
        {
            'name': 'Githurai Stage',
            'location': 'Githurai 45, Kiambu',
            'county': 'kiambu',
            'description': 'Stage at Githurai market'
        },
        {
            'name': 'Kahawa West Stage',
            'location': 'Kahawa West, Nairobi',
            'county': 'nairobi',
            'description': 'Stage serving Kahawa West area'
        }
    ]
    
    from stages.models import Organization
    from datetime import date
    
    # Get or create a default organization
    org, created = Organization.objects.get_or_create(
        name='Kwa Stage Boda Boda Association',
        defaults={
            'organization_type': 'welfare_society',
            'description': 'Main Boda Boda welfare organization',
            'registration_number': 'KSBBA001',
            'phone_number': '+254700000000',
            'email': 'info@kwastage.co.ke',
            'county': 'nairobi',
            'sub_county': 'Westlands',
            'town': 'nairobi',
            'address': 'Nairobi, Kenya',
            'admin_user_id': 1  # Assuming superuser exists
        }
    )
    
    for stage_data in sample_stages:
        stage, created = Stage.objects.get_or_create(
            name=stage_data['name'],
            defaults={
                'organization': org,
                'location': stage_data['location'],
                'county': stage_data['county'],
                'description': stage_data['description'],
                'registration_date': date.today(),
            }
        )
        if created:
            print(f"✅ Created stage: {stage.name}")
        else:
            print(f"📍 Stage already exists: {stage.name}")

    print(f"\nTotal stages now: {Stage.objects.count()}")
