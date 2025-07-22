#!/usr/bin/env python
"""
Quick demo script to test 2FA functionality
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bodaboda_welfare.settings')
django.setup()

from django.contrib.auth.models import User
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_static.models import StaticDevice, StaticToken

def create_demo_user():
    """Create a demo user for testing 2FA"""
    username = 'demo_user'
    password = 'SecurePass123!'
    
    # Check if user exists
    if User.objects.filter(username=username).exists():
        print(f"Demo user '{username}' already exists.")
        user = User.objects.get(username=username)
    else:
        # Create new user
        user = User.objects.create_user(
            username=username,
            password=password,
            email='demo@bodaboda.co.ke',
            first_name='Demo',
            last_name='User'
        )
        print(f"Created demo user '{username}' with password '{password}'")
    
    return user

def setup_demo_2fa(user):
    """Setup 2FA for demo user"""
    # Create TOTP device
    device = TOTPDevice.objects.create(
        user=user,
        name='Demo Authenticator',
        confirmed=True  # Pre-confirm for demo
    )
    
    # Create backup tokens
    static_device = StaticDevice.objects.create(
        user=user,
        name='Demo Backup Tokens'
    )
    
    backup_tokens = []
    for i in range(5):  # Create 5 demo backup tokens
        token = StaticToken.random_token()
        StaticToken.objects.create(device=static_device, token=token)
        backup_tokens.append(token)
    
    print(f"\n2FA Setup for {user.username}:")
    print(f"TOTP Secret: {device.bin_key.hex()}")
    print(f"Config URL: {device.config_url}")
    print(f"Backup Tokens: {', '.join(backup_tokens)}")
    
    return device, backup_tokens

def demo_info():
    """Display demo information"""
    print("\n" + "="*60)
    print("🎯 BODA BODA WELFARE SYSTEM - 2FA DEMO")
    print("="*60)
    print("\n📱 Authentication Test URLs:")
    print("   Login:           http://127.0.0.1:8000/auth/login/")
    print("   2FA Setup:       http://127.0.0.1:8000/auth/2fa/setup/")
    print("   Security:        http://127.0.0.1:8000/auth/security/")
    print("   Dashboard:       http://127.0.0.1:8000/dashboard/")
    
    print("\n🔐 Demo Credentials:")
    print("   Username: demo_user")
    print("   Password: SecurePass123!")
    
    print("\n⚡ Quick Tests:")
    print("   1. Login with demo credentials")
    print("   2. Enable 2FA (scan QR code)")
    print("   3. Logout and re-login")
    print("   4. Test 2FA verification")
    print("   5. Test backup recovery codes")
    
    print("\n🛠️ Management Commands:")
    print("   Check 2FA Status: python manage.py check_2fa_status")
    print("   Check Demo User:  python manage.py check_2fa_status --username demo_user")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    print("Setting up 2FA demo environment...")
    
    # Create demo user
    demo_user = create_demo_user()
    
    # Display demo information
    demo_info()
    
    # Ask if user wants to pre-setup 2FA
    setup_2fa = input("\nWould you like to pre-setup 2FA for testing? (y/n): ").lower()
    
    if setup_2fa == 'y':
        device, tokens = setup_demo_2fa(demo_user)
        print("\n✅ 2FA has been pre-configured for demo_user")
        print("⚠️  Note: In production, users must scan QR codes themselves")
    
    print("\n🚀 Demo environment ready! Start the server and test 2FA functionality.")
    print("   Command: python manage.py runserver")
