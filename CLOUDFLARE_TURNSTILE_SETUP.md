# Cloudflare Turnstile Setup Guide

## 🛡️ About Cloudflare Turnstile

Cloudflare Turnstile is a privacy-preserving alternative to CAPTCHAs that helps protect your website from bots and spam while providing a better user experience.

## 🔧 Development Setup (Current Configuration)

For **localhost development**, we're using Cloudflare's test keys:

```env
CLOUDFLARE_TURNSTILE_SITE_KEY=1x00000000000000000000AA
CLOUDFLARE_TURNSTILE_SECRET_KEY=1x0000000000000000000000000000000AA
```

These test keys:
- ✅ Work on any domain including localhost
- ✅ Always return success for valid challenges
- ✅ Perfect for development and testing

## 🌐 Production Setup

For **production deployment**, you need to:

### Step 1: Create Cloudflare Account
1. Go to https://cloudflare.com/
2. Sign up or log in to your account

### Step 2: Add Your Domain
1. Add your domain to Cloudflare
2. Follow the DNS configuration steps

### Step 3: Generate Turnstile Keys
1. Go to Cloudflare Dashboard
2. Navigate to **Security** → **Turnstile**
3. Click **Add Site**
4. Fill in the details:
   - **Site Name**: Your website name
   - **Domain**: Your actual domain (e.g., yoursite.com, www.yoursite.com)
   - **Widget Mode**: Managed (recommended)
5. Click **Create**
6. Copy the generated Site Key and Secret Key

### Step 4: Update Production Environment
Replace the test keys in your production `.env`:

```env
CLOUDFLARE_TURNSTILE_SITE_KEY=your_production_site_key
CLOUDFLARE_TURNSTILE_SECRET_KEY=your_production_secret_key
```

## 🔍 Key Differences

| Environment | Site Key Format | Works On | Purpose |
|-------------|----------------|----------|---------|
| **Development** | `1x00000000000000000000AA` | Any domain | Testing |
| **Production** | `0x4AAAAAAA...` or custom | Specific domains | Live protection |

## 🚨 Common Issues & Solutions

### Issue: "Invalid domain" Error
**Cause**: Using production keys on localhost or vice versa

**Solution**:
- Development: Use test keys (`1x00000000000000000000AA`)
- Production: Use domain-specific keys from Cloudflare dashboard

### Issue: Turnstile Widget Not Loading
**Check**:
1. Site key is correctly set in templates
2. Cloudflare script is loaded: `https://challenges.cloudflare.com/turnstile/v0/api.js`
3. Network connectivity to Cloudflare

### Issue: Verification Always Fails
**Check**:
1. Secret key matches the site key
2. Domain configuration in Cloudflare dashboard
3. Network connectivity for server-side verification

## 🎯 Testing Your Setup

1. **Run the check script**:
   ```bash
   python check_cloudflare.py
   ```

2. **Test in browser**:
   - Visit http://localhost:8000/register/
   - Look for the Turnstile challenge widget
   - Complete the challenge and submit the form

3. **Check browser console**:
   - No JavaScript errors related to Turnstile
   - Widget loads properly

## 📱 Mobile Considerations

Turnstile works automatically on mobile devices and provides an even better user experience compared to traditional CAPTCHAs.

## 🔐 Security Benefits

- **Privacy-preserving**: No tracking of users
- **Better UX**: Usually invisible to legitimate users
- **Bot protection**: Advanced detection algorithms
- **GDPR compliant**: No personal data collection

## 📞 Need Help?

If you encounter issues:
1. Check the Cloudflare Turnstile documentation
2. Verify your domain configuration in Cloudflare dashboard
3. Test with the provided development keys first
4. Contact Cloudflare support for production issues
