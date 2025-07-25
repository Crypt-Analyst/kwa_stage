#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bodaboda_welfare.settings')
django.setup()

from stages.models import Organization, Stage
from django.contrib.auth.models import User

def create_default_stages():
    try:
        print("🏍️  Creating Default Boda Boda Stages...")
        
        # Ensure we have at least one user for admin
        if not User.objects.exists():
            admin_user = User.objects.create_user('admin', 'admin@kwastage.ke', 'admin123')
            print("✅ Created admin user")
        else:
            admin_user = User.objects.first()
            print(f"✅ Using existing user: {admin_user.username}")
        
        # Create a default organization first
        organization, created = Organization.objects.get_or_create(
            name="KwaStage Boda Boda Welfare",
            defaults={
                'organization_type': 'welfare_society',
                'registration_number': 'KWS-001-2025',
                'description': 'Main boda boda welfare organization',
                'phone_number': '+254700000000',
                'email': 'info@kwastage.ke',
                'county': 'nairobi',
                'sub_county': 'Nairobi Central',
                'town': 'nairobi',
                'address': 'Nairobi, Kenya',
                'admin_user': admin_user
            }
        )
        
        if created:
            print(f"✅ Created organization: {organization.name}")
        else:
            print(f"✅ Using existing organization: {organization.name}")
        
        # Common Kenyan boda boda stages/locations
        stage_data = [
            # Nairobi
            ("Kencom Stage", "Kencom Bus Station, Nairobi CBD", "nairobi", "Nairobi Central"),
            ("Archives Stage", "Kenya National Archives, Nairobi", "nairobi", "Nairobi Central"),
            ("Railway Station", "Nairobi Railway Station", "nairobi", "Nairobi Central"),
            ("Stage 48", "Stage 48, Nairobi", "nairobi", "Nairobi Central"),
            ("Koja Stage", "Koja, Nairobi", "nairobi", "Dagoretti"),
            ("Kawangware Stage", "Kawangware Market", "nairobi", "Dagoretti"),
            ("Kibera Stage", "Kibera, Nairobi", "nairobi", "Kibra"),
            ("Machakos Stage", "Machakos Country Bus Station", "nairobi", "Nairobi Central"),
            ("Globe Cinema Stage", "Globe Cinema Roundabout", "nairobi", "Nairobi Central"),
            ("Nyayo Stadium Stage", "Nyayo National Stadium", "nairobi", "Embakasi South"),
            
            # Mombasa
            ("Digo Road Stage", "Digo Road, Mombasa", "mombasa", "Mvita"),
            ("Buxton Stage", "Buxton, Mombasa", "mombasa", "Jomba"),
            ("Bamburi Stage", "Bamburi, Mombasa", "mombasa", "Kisauni"),
            ("Likoni Stage", "Likoni Ferry, Mombasa", "mombasa", "Likoni"),
            
            # Kisumu
            ("Kisumu Bus Park", "Kisumu Bus Park", "kisumu", "Kisumu Central"),
            ("Kondele Stage", "Kondele Market, Kisumu", "kisumu", "Kisumu West"),
            ("Nyamasaria Stage", "Nyamasaria, Kisumu", "kisumu", "Kisumu West"),
            
            # Nakuru
            ("Nakuru Stage", "Nakuru Town", "nakuru", "Nakuru Town East"),
            ("Afraha Stadium Stage", "Afraha Stadium, Nakuru", "nakuru", "Nakuru Town East"),
            
            # Eldoret
            ("Eldoret Stage", "Eldoret Town", "uasin_gishu", "Eldoret East"),
            ("Langas Stage", "Langas, Eldoret", "uasin_gishu", "Eldoret West"),
            
            # Thika
            ("Thika Stage", "Thika Town", "kiambu", "Thika Town"),
            ("Blue Post Stage", "Blue Post Hotel, Thika", "kiambu", "Thika Town"),
            
            # Machakos
            ("Machakos Town Stage", "Machakos Town", "machakos", "Machakos Town"),
            
            # General/Other
            ("Custom Stage", "Add your own stage location", "nairobi", "Custom Location"),
        ]
        
        created_count = 0
        for stage_name, location, county, sub_county in stage_data:
            stage, created = Stage.objects.get_or_create(
                name=stage_name,
                organization=organization,
                defaults={
                    'location': location,
                    'county': county,
                    'sub_county': sub_county,
                    'description': f'Boda boda stage at {location}',
                    'is_active': True
                }
            )
            
            if created:
                created_count += 1
                print(f"✅ Created stage: {stage_name}")
        
        total_stages = Stage.objects.count()
        print(f"\n📊 Summary:")
        print(f"   - Total stages in database: {total_stages}")
        print(f"   - New stages created: {created_count}")
        print(f"   - Organization: {organization.name}")
        
        print(f"\n🎉 Stages successfully populated!")
        print(f"📍 Users can now select from {total_stages} predefined stages")
        print(f"📝 'Custom Stage' option allows users to add their own location")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating stages: {e}")
        return False

if __name__ == "__main__":
    create_default_stages()
