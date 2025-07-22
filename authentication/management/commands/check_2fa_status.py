from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_static.models import StaticDevice, StaticToken


class Command(BaseCommand):
    help = 'Display 2FA status for all users in the system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Check specific user by username',
        )
        parser.add_argument(
            '--show-tokens',
            action='store_true',
            help='Show backup tokens for users (admin only)',
        )

    def handle(self, *args, **options):
        username = options.get('username')
        show_tokens = options.get('show_tokens')

        if username:
            try:
                user = User.objects.get(username=username)
                users = [user]
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'User "{username}" not found.')
                )
                return
        else:
            users = User.objects.all()

        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('2FA Security Status Report'))
        self.stdout.write('='*60)

        users_with_2fa = 0
        total_users = len(users)

        for user in users:
            # Check if user has 2FA enabled
            totp_devices = user.totpdevice_set.filter(confirmed=True)
            static_devices = user.staticdevice_set.all()
            
            has_2fa = totp_devices.exists()
            if has_2fa:
                users_with_2fa += 1

            # Display user info
            self.stdout.write(f'\nUser: {user.username}')
            if user.first_name or user.last_name:
                self.stdout.write(f'Name: {user.first_name} {user.last_name}')
            
            status = self.style.SUCCESS('✓ ENABLED') if has_2fa else self.style.ERROR('✗ DISABLED')
            self.stdout.write(f'2FA Status: {status}')
            
            if has_2fa:
                self.stdout.write(f'TOTP Devices: {totp_devices.count()}')
                
                # Show backup tokens count
                total_tokens = sum(device.token_set.count() for device in static_devices)
                self.stdout.write(f'Backup Tokens: {total_tokens} remaining')
                
                # Show tokens if requested and for admin users
                if show_tokens and user.is_staff:
                    for device in static_devices:
                        tokens = device.token_set.all()
                        if tokens:
                            self.stdout.write('  Backup Codes:')
                            for token in tokens:
                                self.stdout.write(f'    {token.token}')
            
            self.stdout.write('-' * 40)

        # Summary
        self.stdout.write(f'\n📊 SUMMARY:')
        self.stdout.write(f'Total Users: {total_users}')
        self.stdout.write(f'2FA Enabled: {users_with_2fa}')
        self.stdout.write(f'2FA Disabled: {total_users - users_with_2fa}')
        
        security_percentage = (users_with_2fa / total_users * 100) if total_users > 0 else 0
        self.stdout.write(f'Security Coverage: {security_percentage:.1f}%')
        
        if security_percentage < 50:
            self.stdout.write(
                self.style.WARNING('\n⚠️  Security Alert: Less than 50% of users have 2FA enabled!')
            )
        elif security_percentage < 80:
            self.stdout.write(
                self.style.WARNING('\n⚠️  Recommendation: Encourage more users to enable 2FA')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('\n✅ Good: Most users have 2FA protection enabled')
            )
        
        self.stdout.write('\n' + '='*60)
