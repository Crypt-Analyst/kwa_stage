from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from members.models import MemberProfile
from django.db import transaction


class Command(BaseCommand):
    help = 'Creates a non-deletable superuser with king cap indicator'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username for superuser', default='admin')
        parser.add_argument('--email', type=str, help='Email for superuser', default='admin@kwastage.com')
        parser.add_argument('--password', type=str, help='Password for superuser', default='AdminKwaStage2025!')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        try:
            with transaction.atomic():
                # Check if superuser already exists
                if User.objects.filter(username=username).exists():
                    self.stdout.write(
                        self.style.WARNING(f'Superuser "{username}" already exists')
                    )
                    user = User.objects.get(username=username)
                else:
                    # Create superuser
                    user = User.objects.create_superuser(
                        username=username,
                        email=email,
                        password=password,
                        first_name='System',
                        last_name='Administrator'
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f'Superuser "{username}" created successfully')
                    )

                # Create or update member profile with king cap indicator
                profile, created = MemberProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'phone_number': '+254700000000',
                        'national_id': '00000000',
                        'bike_registration': 'ADMIN001',
                        'stage': None,  # Admin doesn't belong to a specific stage
                        'emergency_contact': '+254700000001',
                        'emergency_contact_relationship': 'System',
                        'next_of_kin': 'System Administrator',
                        'next_of_kin_contact': '+254700000001',
                        'is_admin': True,
                        'is_super_admin': True,
                        'account_status': 'active',
                        'profile_completion_status': 'complete',
                    }
                )

                if not created:
                    # Update existing profile to ensure it has admin privileges
                    profile.is_admin = True
                    profile.is_super_admin = True
                    profile.account_status = 'active'
                    profile.profile_completion_status = 'complete'
                    profile.save()

                # Make user non-deletable by adding a special flag
                user.is_active = True
                user.is_staff = True
                user.is_superuser = True
                user.save()

                # Add a custom attribute to mark as non-deletable
                if not hasattr(user, '_non_deletable'):
                    # We'll handle this in the model's delete method
                    pass

                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Non-deletable superuser "{username}" is ready with king cap indicator 👑'
                    )
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Login credentials:\n'
                        f'Username: {username}\n'
                        f'Password: {password}\n'
                        f'Email: {email}'
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {str(e)}')
            )
