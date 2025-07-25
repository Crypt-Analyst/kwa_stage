# 🏍️ Kwa Stage - Boda Boda Welfare & Emergency Support System

[![Django](https://img.shields.io/badge/Django-5.2.4-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> *"Stage ni yetu, sauti ni yao — we just build the mic"*

A comprehensive Django web application for managing Boda Boda (motorcycle taxi) welfare, emergency support, and community management system. This system provides complete support for riders and their families with modern security features and mobile-responsive design.

## 🚀 Features

### 🛡️ Advanced Security
- **Email Verification**: Mandatory email verification for all new accounts
- **Two-Factor Authentication (2FA)**: TOTP-based authentication with QR codes
- **Google Sign-In**: Social authentication integration
- **Password Reset**: Secure token-based password recovery
- **Session Management**: Secure session handling and logout

### 👥 Member Management
- **Rider Registration**: Comprehensive member profiles
- **Family Support**: Next-of-kin and emergency contact management
- **Profile Management**: Complete member information tracking
- **Stage Organization**: Stage-based member grouping

### 💰 Financial Management
- **Contributions**: Weekly/monthly payment tracking
- **Emergency Fund**: Death and emergency support fund
- **Loan System**: Member loan facility with interest calculation
- **Payment Integration**: M-Pesa integration ready
- **Financial Analytics**: Comprehensive reporting

### 🚨 Emergency & Safety
- **Accident Reporting**: Real-time accident alerts
- **Emergency Response**: Quick emergency contact system
- **Safety Training**: Safety education and resources
- **Insurance Integration**: Ready for insurance partner APIs

### 🏍️ Asset Management
- **Bike Registration**: Complete motorcycle ownership records
- **Asset Protection**: Bike security and tracking
- **Maintenance Records**: Service and repair tracking

### 📱 Communication & Social
- **Notifications**: SMS and email alert system
- **Social Platform**: Community interaction features
- **Job Board**: Job posting and matching system
- **Messaging**: Internal communication system

### 📊 Analytics & Reporting
- **Dashboard**: Comprehensive analytics dashboard
- **Financial Reports**: Payment and contribution tracking
- **Member Statistics**: Community growth metrics
- **Emergency Reports**: Safety and incident analytics

## 🛠️ Technology Stack

- **Backend**: Django 5.2.4, Python 3.13
- **Database**: PostgreSQL (SQLite for development)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5.3
- **Authentication**: Django-OTP, PyOTP, QRCode
- **API**: Django REST Framework
- **Styling**: Bootstrap with custom CSS variables
- **Email**: SMTP with Gmail integration

## 📦 Installation

### Prerequisites
- Python 3.13+
- PostgreSQL (for production)
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Crypt-Analyst/kwa_stage.git
   cd kwa_stage
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   # Create .env file with your settings
   cp .env.example .env
   # Edit .env with your database and email settings
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open http://localhost:8000 in your browser
   - Admin panel: http://localhost:8000/admin

## ⚙️ Configuration

### Environment Variables (.env)
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/kwastage

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com

# Security
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# External APIs (Optional)
MPESA_CONSUMER_KEY=your-mpesa-key
MPESA_CONSUMER_SECRET=your-mpesa-secret
SMS_API_KEY=your-sms-api-key
```

## 🏗️ Project Structure

```
kwa_stage/
├── bodaboda_welfare/          # Main Django project
├── authentication/           # Authentication & 2FA
├── members/                  # Member management
├── contributions/            # Payment tracking
├── emergency/               # Emergency fund management
├── accidents/               # Accident reporting
├── bikes/                   # Asset management
├── stages/                  # Stage management
├── loans/                   # Loan system
├── communication/           # Notifications
├── social/                  # Social features
├── safety/                  # Safety training
├── payments/                # Payment processing
├── templates/               # HTML templates
├── static/                  # CSS, JS, images
├── media/                   # User uploads
└── requirements.txt         # Dependencies
```

## 📱 Mobile Responsive Design

The application is built with a mobile-first approach:
- **Responsive Sidebar**: Collapsible navigation
- **Touch-Friendly**: Optimized for smartphone use
- **Fast Loading**: Optimized assets and caching
- **Offline Ready**: Progressive Web App features

## 🔐 Security Features

### Email Verification System
- Mandatory email verification for all new accounts
- Account remains inactive until email is verified
- Resend verification functionality
- Secure token-based verification

### Two-Factor Authentication
- TOTP-based 2FA with authenticator apps
- QR code setup for easy configuration
- Backup tokens for account recovery
- Optional but recommended for all users

### Password Security
- Strong password requirements
- Secure password reset with email tokens
- Session management and automatic logout
- CSRF protection on all forms

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, email support@kwastage.com or create an issue in this repository.

## 🙏 Acknowledgments

- Django community for the excellent framework
- Bootstrap team for the responsive UI components
- The Boda Boda community for inspiration and requirements
- All contributors who have helped build this system

---

**Made with ❤️ for the Boda Boda community**

*Empowering riders, supporting families, building stronger communities.*
