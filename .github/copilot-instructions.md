# Boda Boda Welfare & Emergency Support System

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Overview

This is a Django web application for managing a Boda Boda (motorcycle taxi) welfare and emergency support system. The system embodies the principle "Boda Boda is Family - Don't Forget That" and provides comprehensive support for riders and their families.

## Architecture

- **Backend**: Django 5.2.4 with Python 3.13
- **Frontend**: HTML, CSS, JavaScript with Bootstrap 5.3
- **Database**: SQLite (development), can be switched to PostgreSQL for production
- **Styling**: Bootstrap with custom CSS using CSS variables
- **Navigation**: Sidebar-based layout for all authenticated pages

## Key Applications

1. **Members**: Rider registration, profiles, and management
2. **Contributions**: Weekly/monthly payments and welfare fund tracking
3. **Emergency**: Death/emergency fund management and family support
4. **Accidents**: Accident reporting and alert system
5. **Bikes**: Bike ownership records and asset protection
6. **Stages**: Stage management and leadership
7. **Loans**: Loan fund/kitty for member support

## Design Principles

- **Family-Centered**: Every feature should reinforce community support
- **Mobile-First**: Responsive design for smartphone access
- **Accessibility**: Clear navigation and user-friendly interfaces
- **Transparency**: Open tracking of funds and support provided
- **Security**: Protect member data and financial information

## Coding Standards

- Use Django best practices and patterns
- Follow PEP 8 for Python code
- Use semantic HTML and accessible markup
- Implement proper error handling and validation
- Add comprehensive comments for complex business logic
- Use Django's built-in security features

## Key Features to Remember

- Sidebar navigation on every authenticated page
- M-Pesa integration for payments
- SMS notifications for alerts
- Family/next-of-kin access for emergencies
- Stage-based member organization
- Comprehensive bike ownership tracking
- Loan fund management with interest calculation

## API Integration Points

- M-Pesa Daraja API for payments
- SMS gateway for notifications
- Potential NHIF/NSSF integrations
- Insurance partner APIs

## Testing Considerations

- Test payment flows thoroughly
- Verify emergency fund calculations
- Ensure proper access controls
- Test mobile responsiveness
- Validate notification systems
