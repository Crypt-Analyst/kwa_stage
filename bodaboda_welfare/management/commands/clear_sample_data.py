from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from members.models import Member, Stage
from contributions.models import Contribution
from emergency.models import EmergencyCase
from accidents.models import AccidentReport
from bikes.models import BikeOwnership
from loans.models import Loan
from financial.models import SaccoProvider, BankProvider, SaccoApplication, BankLoanApplication
from django.db import transaction


class Command(BaseCommand):
    help = 'Clear all sample/test data from the system, keeping only essential configurations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm that you want to delete all user data',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING(
                    'This command will delete ALL user data including:'
                )
            )
            self.stdout.write('- All user accounts (except superusers)')
            self.stdout.write('- All member profiles')
            self.stdout.write('- All contributions')
            self.stdout.write('- All emergency cases')
            self.stdout.write('- All accident reports')
            self.stdout.write('- All bike ownerships')
            self.stdout.write('- All loans')
            self.stdout.write('- All SACCO and bank applications')
            self.stdout.write('')
            self.stdout.write('⚠️  This action CANNOT be undone!')
            self.stdout.write('')
            self.stdout.write('To proceed, run: python manage.py clear_sample_data --confirm')
            return

        with transaction.atomic():
            # Count data before deletion
            user_count = User.objects.filter(is_superuser=False).count()
            member_count = Member.objects.count()
            contribution_count = Contribution.objects.count()
            emergency_count = EmergencyCase.objects.count()
            accident_count = AccidentReport.objects.count()
            bike_count = BikeOwnership.objects.count()
            loan_count = Loan.objects.count()
            sacco_app_count = SaccoApplication.objects.count()
            bank_app_count = BankLoanApplication.objects.count()

            self.stdout.write('🗑️  Clearing sample data...')
            self.stdout.write(f'   Users to delete: {user_count}')
            self.stdout.write(f'   Members to delete: {member_count}')
            self.stdout.write(f'   Contributions to delete: {contribution_count}')
            self.stdout.write(f'   Emergency cases to delete: {emergency_count}')
            self.stdout.write(f'   Accident reports to delete: {accident_count}')
            self.stdout.write(f'   Bike ownerships to delete: {bike_count}')
            self.stdout.write(f'   Loans to delete: {loan_count}')
            self.stdout.write(f'   SACCO applications to delete: {sacco_app_count}')
            self.stdout.write(f'   Bank applications to delete: {bank_app_count}')

            # Delete all dependent data first
            SaccoApplication.objects.all().delete()
            BankLoanApplication.objects.all().delete()
            Loan.objects.all().delete()
            BikeOwnership.objects.all().delete()
            AccidentReport.objects.all().delete()
            EmergencyCase.objects.all().delete()
            Contribution.objects.all().delete()
            Member.objects.all().delete()
            
            # Delete non-superuser accounts
            User.objects.filter(is_superuser=False).delete()

            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('✅ Sample data cleared successfully!'))
            self.stdout.write('')
            self.stdout.write('📋 System is now ready for real users:')
            self.stdout.write(f'   - {Stage.objects.count()} stages configured')
            self.stdout.write(f'   - {SaccoProvider.objects.count()} SACCOs available')
            self.stdout.write(f'   - {BankProvider.objects.count()} banks available')
            self.stdout.write('   - All modules functional and ready')
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('🎉 System ready for production use!'))
