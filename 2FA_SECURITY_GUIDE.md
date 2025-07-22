# Two-Factor Authentication (2FA) Security Upgrade

## Overview
The Boda Boda Welfare System has been enhanced with comprehensive Two-Factor Authentication (2FA) to protect member data, financial transactions, and emergency funds.

## 🔒 Security Features

### **1. TOTP-Based 2FA**
- **Authenticator Apps**: Google Authenticator, Microsoft Authenticator, Authy
- **QR Code Setup**: Easy scanning for device configuration
- **Manual Entry**: Secret key backup for setup issues
- **Time-Based Codes**: 30-second rotating verification codes

### **2. Backup Recovery System**
- **10 Recovery Codes**: Single-use backup tokens
- **Secure Storage**: Download, print, or copy options
- **Regeneration**: New codes can be generated anytime
- **Session Recovery**: Login without authenticator app

### **3. Automatic Protection**
- **Sensitive Operations**: Financial transactions, emergency cases
- **Administrative Functions**: System settings, user management  
- **Session Management**: Auto-logout after inactivity
- **Middleware Protection**: URL-based security enforcement

## 🎯 Protected Operations

### **Mandatory 2FA Required:**
- Financial contributions and payments
- M-Pesa transactions
- Emergency case reporting
- Loan applications and approvals
- Administrative settings
- User data modifications

### **Optional 2FA:**
- Basic profile viewing
- Stage information
- Public announcements
- General navigation

## 🚀 Getting Started

### **For Users:**

1. **Login to System**
   ```
   Visit: http://your-domain/auth/login/
   ```

2. **Enable 2FA**
   - Navigate to: Dashboard → Security Settings → Enable 2FA
   - Scan QR code with authenticator app
   - Verify with 6-digit code
   - Save backup recovery codes

3. **Using 2FA**
   - Login with username/password
   - Enter 6-digit code from authenticator app
   - Or use backup recovery code if needed

### **For Administrators:**

1. **Check 2FA Status**
   ```bash
   python manage.py check_2fa_status
   ```

2. **View Specific User**
   ```bash
   python manage.py check_2fa_status --username john_doe
   ```

3. **Admin Dashboard**
   - Monitor user security compliance
   - View 2FA adoption rates
   - Generate security reports

## 🛡️ Implementation Details

### **URL Protection Configuration**
```python
# settings.py
TWO_FA_REQUIRED_URLS = [
    '/contributions/make-payment/',
    '/emergency/report-case/',
    '/loans/apply/',
    '/admin/',
    '/settings/',
]
```

### **Decorator Usage**
```python
from authentication.decorators import require_2fa, sensitive_operation

# Require 2FA for sensitive views
@require_2fa
def make_payment(request):
    # Payment processing code
    pass

# Always require fresh 2FA verification
@sensitive_operation  
def emergency_fund_withdrawal(request):
    # Critical operation code
    pass
```

### **Template Integration**
```html
<!-- Check if user has 2FA enabled -->
{% if user.totpdevice_set.filter:confirmed=True %}
    <span class="badge bg-success">2FA Enabled</span>
{% else %}
    <a href="{% url 'authentication:two_factor_setup' %}">Enable 2FA</a>
{% endif %}
```

## 📱 Supported Authenticator Apps

### **Recommended Apps:**
- **Google Authenticator** (Android/iOS)
- **Microsoft Authenticator** (Android/iOS)
- **Authy** (Android/iOS/Desktop)
- **1Password** (Premium)
- **LastPass Authenticator**

### **Technical Requirements:**
- TOTP (Time-based One-Time Password)
- RFC 6238 compliance
- 30-second time intervals
- 6-digit codes

## ⚙️ Configuration Options

### **Session Security**
```python
# Auto-logout after 1 hour
SESSION_COOKIE_AGE = 3600
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_HTTPONLY = True
```

### **Password Requirements**
- Minimum 8 characters
- Mixed case letters
- Numbers and special characters
- Not commonly used passwords

### **QR Code Settings**
```python
OTP_TOTP_ISSUER = 'Boda Boda Welfare System'
```

## 🔧 Troubleshooting

### **Common Issues:**

1. **"Invalid verification code"**
   - Check device time synchronization
   - Ensure 6-digit code entry
   - Try backup recovery code

2. **Lost authenticator app**
   - Use backup recovery codes
   - Contact administrator for reset
   - Re-setup 2FA with new device

3. **QR code won't scan**
   - Use manual secret key entry
   - Check camera permissions
   - Try different authenticator app

### **Recovery Process:**
1. Use backup recovery code to login
2. Go to Security Settings
3. Disable current 2FA
4. Re-enable with new device
5. Generate new backup codes

## 📊 Security Monitoring

### **Admin Commands:**
```bash
# Check system-wide 2FA status
python manage.py check_2fa_status

# View user-specific details
python manage.py check_2fa_status --username <username>

# Show backup tokens (admin only)
python manage.py check_2fa_status --show-tokens
```

### **Security Metrics:**
- Total users with 2FA enabled
- Security coverage percentage
- Backup token usage
- Failed verification attempts

## 🚨 Security Best Practices

### **For Users:**
1. ✅ Enable 2FA immediately
2. ✅ Save backup codes securely
3. ✅ Use strong, unique passwords
4. ✅ Log out on shared computers
5. ✅ Keep authenticator app updated

### **For Administrators:**
1. ✅ Monitor 2FA adoption rates
2. ✅ Enforce 2FA for financial operations
3. ✅ Regular security audits
4. ✅ User education and training
5. ✅ Backup and recovery procedures

## 📞 Support

### **User Support:**
- **2FA Setup Issues**: Contact system administrator
- **Lost Access**: Use backup recovery codes
- **Technical Problems**: Check troubleshooting guide

### **Administrator Support:**
- **System Configuration**: Review settings.py
- **User Management**: Use Django admin interface
- **Security Monitoring**: Run check_2fa_status command

## 📝 API Endpoints

### **Authentication URLs:**
```
/auth/login/                    # Enhanced login with 2FA
/auth/2fa/verify/              # 2FA verification step
/auth/2fa/setup/               # Enable/disable 2FA
/auth/2fa/backup-tokens/       # Manage backup codes
/auth/security/                # Security settings dashboard
/auth/logout/                  # Secure logout
```

### **Security Headers:**
- Session timeout protection
- CSRF protection enabled
- Secure cookie settings
- XFrame protection

---

**🛡️ Remember: 2FA significantly improves the security of the Boda Boda Welfare System. Encourage all users to enable it, especially those handling financial transactions and emergency funds.**
