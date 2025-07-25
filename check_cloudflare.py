#!/usr/bin/env python3

import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bodaboda_welfare.settings')

# Setup Django
import django
django.setup()

from decouple import config
from authentication.turnstile import TurnstileVerification, get_turnstile_site_key

def check_cloudflare_setup():
    print("=" * 60)
    print("🔍 CLOUDFLARE TURNSTILE CONFIGURATION CHECK")
    print("=" * 60)
    
    # Check environment variables
    site_key = config('CLOUDFLARE_TURNSTILE_SITE_KEY', default='')
    secret_key = config('CLOUDFLARE_TURNSTILE_SECRET_KEY', default='')
    
    print(f"\n📋 Environment Variables:")
    print(f"   Site Key: {'✅ SET' if site_key else '❌ NOT SET'}")
    print(f"   Secret Key: {'✅ SET' if secret_key else '❌ NOT SET'}")
    
    if site_key:
        print(f"   Site Key Value: {site_key}")
    if secret_key:
        print(f"   Secret Key Value: {secret_key[:20]}...")
    
    # Check Turnstile class
    print(f"\n🛡️  Turnstile Verification:")
    verifier = TurnstileVerification()
    print(f"   Site Key from class: {verifier.site_key}")
    print(f"   Secret Key from class: {'✅ SET' if verifier.secret_key else '❌ NOT SET'}")
    
    # Check template function
    template_key = get_turnstile_site_key()
    print(f"   Template Site Key: {template_key}")
    
    # Domain configuration check
    print(f"\n🌐 Domain Configuration Analysis:")
    if site_key.startswith('0x4AAAAAAA'):
        if site_key == '0x4AAAAAABmZIjj_LgtGhjrw':
            print("   ⚠️  This appears to be a DEMO/TEST site key")
            print("   🔧 This key may only work on specific test domains")
            print("   💡 For localhost testing, you may need different keys")
        else:
            print("   ✅ Custom Cloudflare site key detected")
    else:
        print("   ❌ Invalid site key format")
    
    print(f"\n🚀 Recommendations:")
    if site_key == '0x4AAAAAABmZIjj_LgtGhjrw':
        print("   1. For localhost development, use Cloudflare test keys:")
        print("      Site Key: 1x00000000000000000000AA")
        print("      Secret Key: 1x0000000000000000000000000000000AA")
        print("   2. For production, create proper Cloudflare site keys")
        print("   3. Ensure domain is configured in Cloudflare dashboard")
    
    # Check if running in DEBUG mode
    from django.conf import settings
    print(f"\n⚙️  Current Mode:")
    print(f"   DEBUG Mode: {'✅ ON' if settings.DEBUG else '❌ OFF'}")
    if settings.DEBUG:
        print("   💡 In DEBUG mode, Turnstile verification may be bypassed")

if __name__ == '__main__':
    check_cloudflare_setup()
