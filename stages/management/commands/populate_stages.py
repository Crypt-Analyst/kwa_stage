from django.core.management.base import BaseCommand
from stages.models import Organization, Stage
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Populate database with default boda boda stages'

    def handle(self, *args, **options):
        self.stdout.write("🏍️  Creating Default Boda Boda Stages...")
        
        # Ensure we have at least one user for admin
        if not User.objects.exists():
            admin_user = User.objects.create_user('admin', 'admin@kwastage.ke', 'admin123')
            self.stdout.write("✅ Created admin user")
        else:
            admin_user = User.objects.first()
            self.stdout.write(f"✅ Using existing user: {admin_user.username}")
        
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
            self.stdout.write(f"✅ Created organization: {organization.name}")
        else:
            self.stdout.write(f"✅ Using existing organization: {organization.name}")
        
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
        from datetime import date
        for stage_name, location, county, sub_county in stage_data:
            stage, created = Stage.objects.get_or_create(
                name=stage_name,
                organization=organization,
                defaults={
                    'location': location,
                    'county': county,
                    'sub_county': sub_county,
                    'ward': 'Ward 1',  # Default ward
                    'description': f'Boda boda stage at {location}',
                    'registration_date': date.today(),
                    'is_active': True
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(f"✅ Created stage: {stage_name}")
        
        total_stages = Stage.objects.count()
        self.stdout.write(f"\n📊 Summary:")
        self.stdout.write(f"   - Total stages in database: {total_stages}")
        self.stdout.write(f"   - New stages created: {created_count}")
        self.stdout.write(f"   - Organization: {organization.name}")
        
        self.stdout.write(f"\n🎉 Stages successfully populated!")
        self.stdout.write(f"📍 Users can now select from {total_stages} predefined stages")
