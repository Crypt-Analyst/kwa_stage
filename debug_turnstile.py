#!/usr/bin/env python3

import os
from pathlib import Path

# Load environment from .env file directly
env_file = Path('.env')
env_vars = {}

if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()

def test_env_loading():
    print("=" * 60)
    print("🔍 DIRECT .ENV FILE TESTING")
    print("=" * 60)
    
    # Check if .env exists
    print(f"\n📁 .env file exists: {'✅' if env_file.exists() else '❌'}")
    
    # Check Cloudflare keys in .env
    site_key = env_vars.get('CLOUDFLARE_TURNSTILE_SITE_KEY', '')
    secret_key = env_vars.get('CLOUDFLARE_TURNSTILE_SECRET_KEY', '')
    
    print(f"\n🔑 Cloudflare Keys from .env:")
    print(f"   Site Key: {site_key}")
    print(f"   Secret Key: {secret_key}")
    
    # Validate the keys
    if site_key == '1x00000000000000000000AA' and secret_key == '1x0000000000000000000000000000000AA':
        print(f"   Status: ✅ Correct test keys for localhost")
        return True
    else:
        print(f"   Status: ❌ Wrong keys detected")
        return False

def create_minimal_test_server():
    """Create a minimal test to check Turnstile widget loading"""
    print(f"\n🧪 Creating minimal Turnstile test...")
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloudflare Turnstile Test</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .status {{
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
        }}
        .success {{ background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }}
        .error {{ background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ Cloudflare Turnstile Test</h1>
        
        <div class="status success">
            <strong>✅ Configuration Status:</strong><br>
            Site Key: {env_vars.get('CLOUDFLARE_TURNSTILE_SITE_KEY', 'NOT_SET')}<br>
            Environment: Development (Test Keys)
        </div>
        
        <h3>Turnstile Widget Test:</h3>
        <form method="post" action="#" onsubmit="return testSubmit(event)">
            <!-- Cloudflare Turnstile Widget -->
            <div class="cf-turnstile" 
                 data-sitekey="{env_vars.get('CLOUDFLARE_TURNSTILE_SITE_KEY', '')}"
                 data-theme="light"
                 data-callback="onTurnstileSuccess"
                 data-error-callback="onTurnstileError">
            </div>
            
            <br>
            <button type="submit" style="padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px;">
                Test Submit
            </button>
        </form>
        
        <div id="result" style="margin-top: 20px;"></div>
    </div>

    <!-- Cloudflare Turnstile Script -->
    <script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
    
    <script>
        function onTurnstileSuccess(token) {{
            document.getElementById('result').innerHTML = 
                '<div class="status success"><strong>✅ Turnstile Success!</strong><br>Token received: ' + 
                token.substring(0, 20) + '...</div>';
        }}
        
        function onTurnstileError(error) {{
            document.getElementById('result').innerHTML = 
                '<div class="status error"><strong>❌ Turnstile Error:</strong><br>' + error + '</div>';
        }}
        
        function testSubmit(event) {{
            event.preventDefault();
            const token = document.querySelector('[name="cf-turnstile-response"]');
            if (token && token.value) {{
                document.getElementById('result').innerHTML = 
                    '<div class="status success"><strong>✅ Form Ready!</strong><br>Turnstile token is present and form can be submitted.</div>';
            }} else {{
                document.getElementById('result').innerHTML = 
                    '<div class="status error"><strong>❌ No Token!</strong><br>Turnstile verification not completed.</div>';
            }}
            return false;
        }}
        
        // Check if Turnstile script loaded
        window.addEventListener('load', function() {{
            setTimeout(function() {{
                if (typeof turnstile === 'undefined') {{
                    document.getElementById('result').innerHTML = 
                        '<div class="status error"><strong>❌ Script Error:</strong><br>Cloudflare Turnstile script failed to load.</div>';
                }}
            }}, 3000);
        }});
    </script>
</body>
</html>'''
    
    with open('turnstile_test.html', 'w') as f:
        f.write(html_content)
    
    print(f"   📄 Created: turnstile_test.html")
    print(f"   🌐 Open this file in your browser to test Turnstile widget")

if __name__ == '__main__':
    keys_ok = test_env_loading()
    create_minimal_test_server()
    
    print(f"\n🚀 Next Steps:")
    if keys_ok:
        print(f"   1. Open turnstile_test.html in your browser")
        print(f"   2. Check if the Turnstile widget loads")
        print(f"   3. Complete the challenge and test submit")
        print(f"   4. If this works, restart your Django server: python manage.py runserver")
    else:
        print(f"   1. Fix the .env file configuration first")
        print(f"   2. Ensure test keys are properly set")
