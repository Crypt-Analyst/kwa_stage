# Boda Boda Welfare & Emergency Support System
## Complete System Documentation

### Table of Contents
1. [System Overview](#system-overview)
2. [Core Philosophy](#core-philosophy)
3. [Technical Architecture](#technical-architecture)
4. [Key Features](#key-features)
5. [Module Documentation](#module-documentation)
6. [User Roles & Permissions](#user-roles--permissions)
7. [Installation & Setup](#installation--setup)
8. [API Documentation](#api-documentation)
9. [Security Features](#security-features)
10. [Deployment Guide](#deployment-guide)
11. [Maintenance & Support](#maintenance--support)

---

## System Overview

The **Boda Boda Welfare & Emergency Support System** is a comprehensive digital platform designed to support motorcycle taxi (Boda Boda) riders and their families in Kenya. Built on the principle that "Boda Boda is Family - Don't Forget That," this system provides a complete ecosystem for welfare management, emergency support, financial inclusion, and community building.

### Mission Statement
To create a sustainable, technology-driven support network that ensures no Boda Boda rider or their family faces emergencies alone, while promoting financial inclusion and community solidarity.

### Target Users
- **Primary**: Boda Boda riders and their families
- **Secondary**: Stage officials, SACCO representatives, financial institutions
- **Tertiary**: Government agencies, insurance companies, NGOs

---

## Core Philosophy

### "Boda Boda is Family - Don't Forget That"
This principle drives every feature and decision in the system:

1. **Collective Responsibility**: Every member contributes to and benefits from the welfare fund
2. **Emergency Response**: Immediate support for accidents, death, and medical emergencies
3. **Financial Inclusion**: Access to loans, savings, and financial services
4. **Community Building**: Social features that strengthen bonds between riders
5. **Transparency**: Open tracking of all contributions and support provided

---

## Technical Architecture

### Technology Stack
- **Backend Framework**: Django 5.2.4 (Python 3.13)
- **Database**: PostgreSQL (Supabase) for production, SQLite for development
- **Frontend**: HTML5, CSS3, JavaScript with Bootstrap 5.3
- **Authentication**: Django OTP with Two-Factor Authentication
- **File Storage**: Django file system (configurable for cloud storage)
- **APIs**: Django REST Framework for API endpoints
- **Payment Integration**: M-Pesa Daraja API
- **SMS Gateway**: AfricasTalking API
- **Deployment**: Docker-ready with production configurations

### System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   Database      │
│   (Bootstrap)   │◄──►│   (Django)      │◄──►│   (PostgreSQL)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Mobile UI     │    │   External APIs │    │   File Storage  │
│   (Responsive)  │    │   (M-Pesa, SMS) │    │   (Media Files) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## Key Features

### 1. Member Management System
- **Registration & Profiles**: Complete member registration with KYC
- **Stage Management**: Organize members by geographical stages
- **Family Tracking**: Next-of-kin and dependent information
- **Document Management**: ID cards, licenses, certificates
- **Online Status**: Real-time member activity tracking

### 2. Welfare & Emergency Support
- **Emergency Fund**: Pooled community fund for emergencies
- **Death Benefits**: Immediate support for families of deceased members
- **Medical Emergency**: Quick response fund for accidents and illnesses
- **Emergency Reporting**: 24/7 emergency case reporting system
- **Family Access**: Emergency contact system for families

### 3. Financial Inclusion Platform
- **Loan Management**: Member-to-member and institutional loans
- **SACCO Integration**: Connection with local SACCOs
- **Bank Partnerships**: Integration with banking services
- **Digital Wallet**: E-wallet for transactions and payments
- **Contribution Tracking**: Automated welfare contribution management
- **Financial Analytics**: Personal and community financial insights

### 4. Safety & Compliance
- **Accident Reporting**: Comprehensive accident documentation
- **Insurance Tracking**: Policy management and renewals
- **License Management**: Driving license and permit tracking
- **Safety Training**: Training program management
- **Incident Analytics**: Safety pattern analysis and reporting

### 5. Communication & Social Features
- **Group Messaging**: Stage-based and topic-based chat groups
- **Social Feed**: Community news and updates
- **Event Management**: Community events and meetings
- **Notification System**: SMS and in-app notifications
- **Emergency Alerts**: Broadcast emergency communications

### 6. Payment & Transaction System
- **M-Pesa Integration**: Direct mobile money transactions
- **Digital Tokens**: Prepaid token system for services
- **Transaction History**: Complete audit trail of all transactions
- **Multi-currency Support**: KES primary, USD for international
- **Payment Scheduling**: Automated recurring payments

---

## Module Documentation

### Members Module (`members/`)
**Purpose**: Core member management and authentication

**Key Models**:
- `Member`: Primary member profile with KYC information
- `SaccoAffiliation`: SACCO membership tracking
- `MemberDocument`: Document storage and verification

**Key Features**:
- Profile setup and management
- Stage assignment and management
- Next-of-kin tracking
- Document upload and verification
- Online status monitoring

**API Endpoints**:
- `GET /api/members/` - List all members
- `POST /api/members/` - Create new member
- `GET /api/members/{id}/` - Get member details
- `PUT /api/members/{id}/` - Update member
- `POST /api/members/{id}/upload-document/` - Upload document

### Contributions Module (`contributions/`)
**Purpose**: Welfare fund management and contribution tracking

**Key Models**:
- `Contribution`: Individual member contributions
- `WelfareAccount`: Community welfare fund tracking
- `ContributionSchedule`: Automated contribution scheduling

**Key Features**:
- Weekly/monthly contribution collection
- Welfare fund balance tracking
- Contribution history and analytics
- Automated reminders and notifications
- Multi-payment method support

### Emergency Module (`emergency/`)
**Purpose**: Emergency case management and response

**Key Models**:
- `EmergencyCase`: Emergency incident tracking
- `EmergencyFund`: Emergency fund disbursement
- `EmergencyContact`: Emergency contact management

**Key Features**:
- 24/7 emergency reporting
- Immediate fund disbursement
- Family notification system
- Emergency case tracking
- Support documentation

### Financial Module (`financial/`)
**Purpose**: Financial services and loan management

**Key Models**:
- `BankProvider`: Banking partner information
- `SaccoProvider`: SACCO partnership details
- `LoanApplication`: Loan request and approval workflow

**Key Features**:
- Bank and SACCO integration
- Loan application and approval
- Interest calculation and management
- Credit scoring and assessment
- Financial product recommendations

### Payments Module (`payments/`)
**Purpose**: Payment processing and wallet management

**Key Models**:
- `EWallet`: Digital wallet for each member
- `WalletTransaction`: Transaction history
- `PaymentMethod`: Supported payment methods
- `DigitalToken`: Prepaid token system

**Key Features**:
- M-Pesa integration
- Digital wallet management
- Transaction processing
- Payment method management
- Token-based payments

### Safety Module (`safety/`)
**Purpose**: Safety compliance and incident management

**Key Models**:
- `Insurance`: Insurance policy tracking
- `DrivingLicense`: License management
- `SafetyTraining`: Training program tracking
- `SafetyIncident`: Incident reporting and analysis

**Key Features**:
- Insurance policy management
- License renewal tracking
- Safety training programs
- Incident reporting and analysis
- Compliance monitoring

### Social Module (`social/`)
**Purpose**: Community building and communication

**Key Models**:
- `Post`: Social media posts
- `GroupChat`: Group messaging
- `Comment`: Post comments and interactions
- `Event`: Community event management

**Key Features**:
- Social media feed
- Group messaging
- Event organization
- Community interactions
- Content moderation

### Stages Module (`stages/`)
**Purpose**: Geographical organization and management

**Key Models**:
- `Stage`: Boda Boda stages (pickup points)
- `Organization`: Stage management organization
- `StageOfficial`: Stage leadership tracking

**Key Features**:
- Stage registration and management
- GPS location tracking
- Stage official management
- Inter-stage communication
- Resource allocation

---

## User Roles & Permissions

### 1. Regular Member
**Permissions**:
- View own profile and update personal information
- Make contributions and view contribution history
- Report emergencies and view emergency status
- Apply for loans and financial services
- Access safety training and insurance information
- Participate in social activities and messaging

**Restrictions**:
- Cannot access other members' sensitive information
- Cannot approve loans or emergency funds
- Cannot modify system-wide settings

### 2. Stage Official
**Permissions**:
- All regular member permissions
- View stage member information
- Approve emergency cases within limits
- Manage stage events and communications
- Access stage-level analytics and reports

**Restrictions**:
- Limited to own stage members
- Cannot access financial system settings
- Cannot approve large emergency disbursements

### 3. Financial Officer
**Permissions**:
- All regular member permissions
- Approve loan applications
- Manage welfare fund distributions
- Access financial analytics and reports
- Configure payment methods and rates

**Restrictions**:
- Cannot access member personal information unrelated to finances
- Cannot modify core system settings

### 4. System Administrator
**Permissions**:
- Full system access
- User management and role assignment
- System configuration and settings
- API key management
- Database administration
- Security configuration

### 5. Emergency Coordinator
**Permissions**:
- All regular member permissions
- Access all emergency cases
- Approve emergency fund disbursements
- Coordinate with external emergency services
- Manage emergency contact networks

---

## Installation & Setup

### Prerequisites
- Python 3.13+
- PostgreSQL 12+
- Git
- Node.js (for asset compilation)
- Redis (for caching and background tasks)

### Development Setup

1. **Clone Repository**
```bash
git clone https://github.com/Crypt-Analyst/kwa_stage.git
cd kwa_stage
```

2. **Create Virtual Environment**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Configuration**
Create `.env` file:
```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/kwastage
DEBUG=True
SECRET_KEY=your-secret-key-here

# External APIs
MPESA_CONSUMER_KEY=your-mpesa-consumer-key
MPESA_CONSUMER_SECRET=your-mpesa-consumer-secret
MPESA_PASSKEY=your-mpesa-passkey
MPESA_SHORTCODE=your-shortcode

# SMS Configuration
SMS_API_KEY=your-sms-api-key
SMS_USERNAME=your-sms-username

# Email Configuration
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Google Maps (Optional)
GOOGLE_MAPS_API_KEY=your-google-maps-key
```

5. **Database Setup**
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

6. **Load Sample Data** (Optional)
```bash
python manage.py populate_stages
python manage.py populate_financial_providers
```

7. **Run Development Server**
```bash
python manage.py runserver
```

### Production Deployment

1. **Docker Deployment**
```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "bodaboda_welfare.wsgi:application"]
```

2. **Docker Compose**
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://user:pass@db:5432/kwastage
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: kwastage
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  postgres_data:
```

---

## API Documentation

### Authentication
All API endpoints require authentication using Django's session authentication or token-based authentication.

**Headers Required**:
```
Authorization: Bearer <token>
Content-Type: application/json
X-CSRFToken: <csrf_token>  # For session auth
```

### Core Endpoints

#### Members API
```
GET    /api/members/                    # List members
POST   /api/members/                    # Create member
GET    /api/members/{id}/               # Get member details
PUT    /api/members/{id}/               # Update member
DELETE /api/members/{id}/               # Deactivate member
POST   /api/members/{id}/upload-photo/  # Upload profile photo
```

#### Contributions API
```
GET    /api/contributions/              # List contributions
POST   /api/contributions/              # Make contribution
GET    /api/contributions/{id}/         # Get contribution details
GET    /api/welfare-fund/balance/       # Get welfare fund balance
GET    /api/contributions/analytics/    # Get contribution analytics
```

#### Emergency API
```
GET    /api/emergencies/               # List emergency cases
POST   /api/emergencies/               # Report emergency
GET    /api/emergencies/{id}/          # Get emergency details
PUT    /api/emergencies/{id}/approve/  # Approve emergency fund
POST   /api/emergencies/{id}/update/   # Update emergency status
```

#### Financial API
```
GET    /api/banks/                     # List bank providers
GET    /api/saccos/                    # List SACCO providers
POST   /api/loans/apply/               # Apply for loan
GET    /api/loans/                     # List user's loans
GET    /api/loans/{id}/                # Get loan details
POST   /api/loans/{id}/approve/        # Approve loan (admin)
```

#### Payments API
```
GET    /api/wallet/                    # Get wallet details
POST   /api/wallet/topup/              # Top up wallet
POST   /api/wallet/withdraw/           # Withdraw from wallet
GET    /api/wallet/transactions/       # Get transaction history
POST   /api/payments/mpesa/            # Process M-Pesa payment
```

### Webhook Endpoints
```
POST   /api/webhooks/mpesa/            # M-Pesa payment callback
POST   /api/webhooks/sms/              # SMS delivery status
POST   /api/webhooks/emergency/        # External emergency alerts
```

---

## Security Features

### 1. Authentication & Authorization
- **Multi-Factor Authentication**: SMS-based 2FA for sensitive operations
- **Role-Based Access Control**: Granular permissions based on user roles
- **Session Management**: Secure session handling with timeout
- **Password Security**: Strong password requirements and hashing

### 2. Data Protection
- **Encryption**: Sensitive data encrypted at rest and in transit
- **PII Protection**: Personal information handling compliance
- **Audit Trails**: Complete logging of all system activities
- **Data Backup**: Automated daily backups with retention policies

### 3. API Security
- **Rate Limiting**: API call limits to prevent abuse
- **CORS Configuration**: Proper cross-origin resource sharing setup
- **CSRF Protection**: Cross-site request forgery protection
- **Input Validation**: Comprehensive input sanitization

### 4. Infrastructure Security
- **HTTPS Enforcement**: SSL/TLS encryption for all communications
- **Database Security**: Connection encryption and access controls
- **File Upload Security**: Virus scanning and file type validation
- **Server Hardening**: Security configurations and monitoring

### 5. Financial Security
- **Transaction Verification**: Multi-step verification for financial transactions
- **Fraud Detection**: Automated fraud pattern detection
- **Reconciliation**: Daily financial reconciliation processes
- **Audit Compliance**: Financial audit trail maintenance

---

## Deployment Guide

### Production Environment Setup

#### 1. Server Requirements
- **CPU**: Minimum 2 cores, Recommended 4+ cores
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: Minimum 20GB SSD, Recommended 100GB+
- **Network**: Stable internet connection with 10Mbps+
- **OS**: Ubuntu 20.04 LTS or CentOS 8+

#### 2. Dependencies Installation
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.13 python3.13-venv python3.13-dev -y

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Install Redis
sudo apt install redis-server -y

# Install Nginx
sudo apt install nginx -y

# Install Git
sudo apt install git -y
```

#### 3. Application Deployment
```bash
# Create application user
sudo useradd -m -s /bin/bash kwastage
sudo su - kwastage

# Clone and setup application
git clone https://github.com/Crypt-Analyst/kwa_stage.git
cd kwa_stage
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with production values

# Setup database
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

#### 4. Nginx Configuration
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /path/to/ssl/cert.pem;
    ssl_certificate_key /path/to/ssl/private.key;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/kwastage/kwa_stage/staticfiles/;
        expires 30d;
    }

    location /media/ {
        alias /home/kwastage/kwa_stage/media/;
        expires 7d;
    }
}
```

#### 5. Systemd Service
```ini
[Unit]
Description=KwaStage Gunicorn Application Server
After=network.target

[Service]
User=kwastage
Group=www-data
WorkingDirectory=/home/kwastage/kwa_stage
Environment="PATH=/home/kwastage/kwa_stage/.venv/bin"
ExecStart=/home/kwastage/kwa_stage/.venv/bin/gunicorn \
    --workers 3 \
    --bind 127.0.0.1:8000 \
    bodaboda_welfare.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

#### 6. SSL Certificate Setup
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com

# Setup auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

#### 7. Monitoring Setup
```bash
# Install monitoring tools
sudo apt install htop iotop netstat-nat -y

# Setup log rotation
sudo nano /etc/logrotate.d/kwastage
# Add log rotation configuration

# Setup backup script
sudo nano /home/kwastage/backup.sh
# Add database and media backup commands

# Schedule backups
sudo crontab -e
# Add: 0 2 * * * /home/kwastage/backup.sh
```

---

## Maintenance & Support

### Daily Operations

#### 1. System Health Checks
```bash
# Check application status
sudo systemctl status kwastage

# Check database connections
sudo -u postgres psql -c "SELECT count(*) FROM pg_stat_activity;"

# Check disk space
df -h

# Check memory usage
free -m

# Check logs
tail -f /var/log/nginx/access.log
tail -f /home/kwastage/kwa_stage/logs/django.log
```

#### 2. Performance Monitoring
- **Response Time**: Monitor API response times
- **Database Performance**: Track query performance and slow queries
- **Memory Usage**: Monitor application memory consumption
- **Disk Usage**: Track storage usage and growth
- **Error Rates**: Monitor application error rates and types

#### 3. Security Monitoring
- **Failed Login Attempts**: Monitor and alert on suspicious login activity
- **API Abuse**: Track unusual API usage patterns
- **File Upload Monitoring**: Monitor uploaded files for security threats
- **SSL Certificate Expiry**: Track certificate expiration dates

### Backup & Recovery

#### 1. Database Backup
```bash
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="kwastage"
BACKUP_DIR="/home/kwastage/backups"

# Create backup
pg_dump $DB_NAME > $BACKUP_DIR/db_backup_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/db_backup_$DATE.sql

# Remove backups older than 30 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
```

#### 2. Media Files Backup
```bash
# Sync media files to remote storage
rsync -av /home/kwastage/kwa_stage/media/ \
    user@backup-server:/backups/kwastage/media/
```

#### 3. Recovery Procedures
```bash
# Database recovery
gunzip -c backup_file.sql.gz | psql kwastage

# Media files recovery
rsync -av user@backup-server:/backups/kwastage/media/ \
    /home/kwastage/kwa_stage/media/

# Application code recovery
git pull origin main
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart kwastage
```

### Update Procedures

#### 1. Application Updates
```bash
# Backup before update
./backup.sh

# Pull latest code
git pull origin main

# Update dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart services
sudo systemctl restart kwastage
sudo systemctl reload nginx
```

#### 2. Security Updates
```bash
# System updates
sudo apt update && sudo apt upgrade -y

# Python security updates
pip list --outdated
pip install --upgrade package_name

# Database updates
sudo apt update postgresql
```

### Troubleshooting

#### Common Issues

1. **Database Connection Errors**
   - Check PostgreSQL service status
   - Verify connection parameters in .env
   - Check firewall settings
   - Review database logs

2. **High Memory Usage**
   - Monitor Django application memory
   - Check for memory leaks in custom code
   - Optimize database queries
   - Consider scaling horizontally

3. **Slow Response Times**
   - Analyze database query performance
   - Check static file serving
   - Monitor network latency
   - Review caching configuration

4. **Payment Integration Issues**
   - Verify M-Pesa API credentials
   - Check webhook endpoints
   - Monitor transaction logs
   - Validate SSL certificates

5. **File Upload Problems**
   - Check media directory permissions
   - Verify file size limits
   - Monitor disk space
   - Review upload validation

#### Log Analysis
```bash
# Application logs
tail -f /home/kwastage/kwa_stage/logs/django.log

# Database logs
sudo tail -f /var/log/postgresql/postgresql-15-main.log

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# System logs
sudo journalctl -f -u kwastage
```

---

## Support & Contact

### Technical Support
- **Email**: support@kwastage.com
- **Phone**: +254 700 000 000
- **Documentation**: https://docs.kwastage.com
- **GitHub Issues**: https://github.com/Crypt-Analyst/kwa_stage/issues

### Community Support
- **User Forum**: https://community.kwastage.com
- **WhatsApp Group**: [Link to community group]
- **Telegram Channel**: @kwastage_support

### Emergency Contacts
- **System Outage**: +254 700 000 001
- **Security Issues**: security@kwastage.com
- **Financial Emergencies**: +254 700 000 002

---

*This documentation is maintained by the KwaStage development team and is updated regularly. Last updated: January 2025*
