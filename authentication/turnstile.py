import requests
from django.conf import settings
from decouple import config


class TurnstileVerification:
    """Cloudflare Turnstile verification utility"""
    
    def __init__(self):
        self.secret_key = config('CLOUDFLARE_TURNSTILE_SECRET_KEY', default='')
        self.site_key = config('CLOUDFLARE_TURNSTILE_SITE_KEY', default='')
        self.verify_url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'
    
    def verify_token(self, token, ip_address=None):
        """
        Verify Turnstile token with Cloudflare
        
        Args:
            token (str): The Turnstile response token
            ip_address (str, optional): User's IP address
            
        Returns:
            dict: Verification result with success status and details
        """
        if not self.secret_key or self.secret_key == 'your-secret-key':
            # In development/sandbox mode, always return success
            if settings.DEBUG:
                return {
                    'success': True,
                    'sandbox': True,
                    'message': 'Sandbox mode - verification bypassed'
                }
            else:
                return {
                    'success': False,
                    'error': 'Turnstile secret key not configured'
                }
        
        if not token:
            return {
                'success': False,
                'error': 'No Turnstile token provided'
            }
        
        data = {
            'secret': self.secret_key,
            'response': token
        }
        
        if ip_address:
            data['remoteip'] = ip_address
        
        try:
            response = requests.post(self.verify_url, data=data, timeout=10)
            result = response.json()
            
            return {
                'success': result.get('success', False),
                'error_codes': result.get('error-codes', []),
                'challenge_ts': result.get('challenge_ts'),
                'hostname': result.get('hostname'),
                'action': result.get('action'),
                'cdata': result.get('cdata')
            }
            
        except requests.RequestException as e:
            return {
                'success': False,
                'error': f'Network error during verification: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Verification error: {str(e)}'
            }


def verify_turnstile(request):
    """
    Helper function to verify Turnstile token from request
    
    Args:
        request: Django request object
        
    Returns:
        dict: Verification result
    """
    verifier = TurnstileVerification()
    token = request.POST.get('cf-turnstile-response') or request.GET.get('cf-turnstile-response')
    ip_address = get_client_ip(request)
    
    return verifier.verify_token(token, ip_address)


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_turnstile_site_key():
    """Get Turnstile site key for templates"""
    return config('CLOUDFLARE_TURNSTILE_SITE_KEY', default='')
