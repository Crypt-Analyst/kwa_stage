from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from stages.models import Organization, Stage


class Command(BaseCommand):
    help = 'Create a default organization and assign existing stages to it'

    def add_arguments(self, parser):
        parser.add_argument(
            '--org-name',
            type=str,
            default='Kwa Stage Boda Boda SACCO',
            help='Name of the default organization to create',
        )
        parser.add_argument(
            '--admin-username',
            type=str,
            help='Username of the admin user for the organization',
        )

    def handle(self, *args, **options):
        org_name = options['org_name']
        admin_username = options.get('admin_username')

        # Get admin user
        if admin_username:
            try:
                admin_user = User.objects.get(username=admin_username)
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Admin user "{admin_username}" not found.')
                )
                return
        else:
            # Try to get first superuser
            admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                # Get first user
                admin_user = User.objects.first()
                if not admin_user:
                    self.stdout.write(
                        self.style.ERROR('No users found in the system. Create a user first.')
                    )
                    return

        # Check if default organization exists
        org, created = Organization.objects.get_or_create(
            name=org_name,
            defaults={
                'organization_type': 'sacco',
                'registration_number': 'SACCO-001-2025',
                'description': 'Default SACCO for Boda Boda welfare system',
                'phone_number': '+254700000000',
                'email': 'info@kwastage.co.ke',
                'county': 'Nairobi',
                'sub_county': 'Westlands',
                'town': 'Nairobi',
                'address': 'Nairobi, Kenya',
                'admin_user': admin_user,
            }
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Created default organization: {org_name}')
            )
        else:
            self.stdout.write(f'Organization "{org_name}" already exists')

        # Assign stages without organization to the default org
        unassigned_stages = Stage.objects.filter(organization__isnull=True)
        count = unassigned_stages.count()

        if count > 0:
            unassigned_stages.update(organization=org)
            self.stdout.write(
                self.style.SUCCESS(f'Assigned {count} stages to {org_name}')
            )
        else:
            self.stdout.write('No unassigned stages found')

        # Display summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write('ORGANIZATION SETUP SUMMARY')
        self.stdout.write('='*50)
        self.stdout.write(f'Organization: {org.name}')
        self.stdout.write(f'Type: {org.get_organization_type_display()}')
        self.stdout.write(f'Admin: {org.admin_user.username}')
        self.stdout.write(f'Total Stages: {org.total_stages()}')
        self.stdout.write(f'Total Members: {org.total_members()}')
        self.stdout.write('='*50)
