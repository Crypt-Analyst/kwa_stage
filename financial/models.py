"""
SACCO and Banking Models for Boda Boda Financial Services
"""
from django.db import models
from django.contrib.auth.models import User
from members.models import Member
import uuid
from datetime import date, timedelta

class SaccoProvider(models.Model):
    """
    Comprehensive SACCO information for boda boda financing
    """
    name = models.CharField(max_length=200, unique=True)
    sacco_code = models.CharField(max_length=20, unique=True)
    
    # Contact Information
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    physical_address = models.TextField()
    
    # Coverage and Service Areas
    coverage_area = models.CharField(max_length=100)  # e.g., "Nationwide", "Western Region"
    counties_served = models.TextField(help_text="Comma-separated list of counties")
    headquarters_location = models.CharField(max_length=100)
    
    # Services Offered
    offers_motorcycle_loans = models.BooleanField(default=True)
    offers_business_loans = models.BooleanField(default=True)
    offers_savings_accounts = models.BooleanField(default=True)
    offers_insurance = models.BooleanField(default=False)
    offers_emergency_fund = models.BooleanField(default=True)
    offers_group_lending = models.BooleanField(default=True)
    
    # Loan Terms
    min_loan_amount = models.DecimalField(max_digits=10, decimal_places=2, default=5000)
    max_loan_amount = models.DecimalField(max_digits=12, decimal_places=2, default=500000)
    interest_rate_min = models.DecimalField(max_digits=5, decimal_places=2, default=12.0)
    interest_rate_max = models.DecimalField(max_digits=5, decimal_places=2, default=24.0)
    max_repayment_period_months = models.IntegerField(default=36)
    
    # Requirements
    minimum_savings_period = models.IntegerField(default=3, help_text="Months")
    requires_guarantors = models.BooleanField(default=True)
    minimum_guarantors = models.IntegerField(default=2)
    requires_collateral = models.BooleanField(default=False)
    
    # SACCO Details
    registration_number = models.CharField(max_length=50)
    license_number = models.CharField(max_length=50, blank=True)
    member_count = models.IntegerField(default=0)
    asset_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Specialization
    specializes_in_transport = models.BooleanField(default=True)
    bodaboda_focused = models.BooleanField(default=True)
    target_demographic = models.CharField(max_length=100, default="Transport Operators")
    
    # Status and Ratings
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_applications_processed = models.IntegerField(default=0)
    success_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Application Process
    application_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    processing_time_days = models.IntegerField(default=7)
    online_application_available = models.BooleanField(default=True)
    
    # Metadata
    description = models.TextField()
    logo = models.ImageField(upload_to='sacco_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "SACCO Provider"
        verbose_name_plural = "SACCO Providers"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.coverage_area})"
    
    def get_interest_rate_range(self):
        return f"{self.interest_rate_min}% - {self.interest_rate_max}%"
    
    def get_loan_amount_range(self):
        return f"KSh {self.min_loan_amount:,.0f} - KSh {self.max_loan_amount:,.0f}"

class BankProvider(models.Model):
    """
    Banking institutions offering boda boda and transport financing
    """
    name = models.CharField(max_length=200, unique=True)
    bank_code = models.CharField(max_length=10, unique=True)
    
    # Contact Information
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField()
    loan_application_url = models.URLField(blank=True, help_text="Direct link to bank's loan application page")
    head_office_address = models.TextField()
    
    # Banking Details
    swift_code = models.CharField(max_length=15, blank=True)
    license_number = models.CharField(max_length=50)
    
    # Coverage
    nationwide_coverage = models.BooleanField(default=True)
    total_branches = models.IntegerField(default=0)
    counties_with_branches = models.TextField(help_text="Comma-separated list")
    
    # Boda Boda Specific Services
    offers_motorcycle_loans = models.BooleanField(default=True)
    offers_business_loans = models.BooleanField(default=True)
    offers_asset_financing = models.BooleanField(default=True)
    offers_savings_accounts = models.BooleanField(default=True)
    offers_current_accounts = models.BooleanField(default=True)
    offers_mobile_banking = models.BooleanField(default=True)
    offers_insurance_products = models.BooleanField(default=False)
    
    # Loan Products for Boda Boda
    motorcycle_loan_min = models.DecimalField(max_digits=10, decimal_places=2, default=50000)
    motorcycle_loan_max = models.DecimalField(max_digits=12, decimal_places=2, default=2000000)
    business_loan_min = models.DecimalField(max_digits=10, decimal_places=2, default=10000)
    business_loan_max = models.DecimalField(max_digits=12, decimal_places=2, default=5000000)
    
    # Interest Rates
    motorcycle_loan_rate_min = models.DecimalField(max_digits=5, decimal_places=2, default=14.0)
    motorcycle_loan_rate_max = models.DecimalField(max_digits=5, decimal_places=2, default=24.0)
    business_loan_rate_min = models.DecimalField(max_digits=5, decimal_places=2, default=16.0)
    business_loan_rate_max = models.DecimalField(max_digits=5, decimal_places=2, default=28.0)
    
    # Repayment Terms
    motorcycle_loan_max_term = models.IntegerField(default=60, help_text="Months")
    business_loan_max_term = models.IntegerField(default=36, help_text="Months")
    
    # Requirements
    minimum_income_requirement = models.DecimalField(max_digits=10, decimal_places=2, default=15000)
    requires_collateral = models.BooleanField(default=True)
    requires_guarantor = models.BooleanField(default=True)
    minimum_age = models.IntegerField(default=18)
    maximum_age = models.IntegerField(default=65)
    
    # Processing
    application_fee = models.DecimalField(max_digits=8, decimal_places=2, default=1000)
    processing_time_days = models.IntegerField(default=14)
    approval_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Digital Services
    online_application = models.BooleanField(default=True)
    mobile_app_available = models.BooleanField(default=True)
    ussd_banking = models.CharField(max_length=20, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_cbb_licensed = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    
    # Metadata
    description = models.TextField()
    logo = models.ImageField(upload_to='bank_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Bank Provider"
        verbose_name_plural = "Bank Providers"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class SaccoApplication(models.Model):
    """
    SACCO membership and loan applications from boda boda riders
    """
    APPLICATION_TYPES = (
        ('membership', 'SACCO Membership'),
        ('motorcycle_loan', 'Motorcycle Loan'),
        ('business_loan', 'Business Loan'),
        ('emergency_loan', 'Emergency Loan'),
        ('group_loan', 'Group Loan'),
    )
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('pending_documents', 'Pending Documents'),
        ('disbursed', 'Disbursed'),
    )
    
    # Basic Info
    application_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    applicant = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='sacco_applications')
    sacco = models.ForeignKey(SaccoProvider, on_delete=models.CASCADE, related_name='applications')
    application_type = models.CharField(max_length=20, choices=APPLICATION_TYPES)
    
    # Application Details
    requested_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    purpose = models.TextField(help_text="Purpose of the loan or membership")
    repayment_period_months = models.IntegerField(null=True, blank=True)
    
    # Personal Information (from form)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2)
    other_income_sources = models.TextField(blank=True)
    dependents_count = models.IntegerField(default=0)
    current_loans = models.TextField(blank=True, help_text="Existing loans and amounts")
    
    # Business Information
    years_in_bodaboda = models.IntegerField()
    daily_earnings = models.DecimalField(max_digits=8, decimal_places=2)
    motorcycle_owned = models.BooleanField(default=False)
    motorcycle_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    route_description = models.TextField()
    stage_location = models.CharField(max_length=200)
    
    # Guarantor Information
    guarantor1_name = models.CharField(max_length=200, blank=True)
    guarantor1_phone = models.CharField(max_length=20, blank=True)
    guarantor1_id_number = models.CharField(max_length=20, blank=True)
    guarantor1_relationship = models.CharField(max_length=100, blank=True)
    
    guarantor2_name = models.CharField(max_length=200, blank=True)
    guarantor2_phone = models.CharField(max_length=20, blank=True)
    guarantor2_id_number = models.CharField(max_length=20, blank=True)
    guarantor2_relationship = models.CharField(max_length=100, blank=True)
    
    # Documents
    id_copy_uploaded = models.BooleanField(default=False)
    kra_pin_uploaded = models.BooleanField(default=False)
    bank_statements_uploaded = models.BooleanField(default=False)
    business_license_uploaded = models.BooleanField(default=False)
    passport_photo_uploaded = models.BooleanField(default=False)
    
    # Status and Processing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    response_from_sacco = models.TextField(blank=True)
    sacco_contact_person = models.CharField(max_length=200, blank=True)
    sacco_contact_phone = models.CharField(max_length=20, blank=True)
    
    # Approval Details
    approved_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    approved_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    approved_term_months = models.IntegerField(null=True, blank=True)
    conditions = models.TextField(blank=True)
    
    # Disbursement
    disbursement_date = models.DateField(null=True, blank=True)
    disbursement_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "SACCO Application"
        verbose_name_plural = "SACCO Applications"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.applicant.user.get_full_name()} - {self.sacco.name} ({self.application_type})"
    
    def get_status_display_with_icon(self):
        status_icons = {
            'draft': '📝',
            'submitted': '📤',
            'under_review': '👀',
            'approved': '✅',
            'rejected': '❌',
            'pending_documents': '📋',
            'disbursed': '💰',
        }
        return f"{status_icons.get(self.status, '📄')} {self.get_status_display()}"

class BankLoanApplication(models.Model):
    """
    Bank loan applications from boda boda riders
    """
    LOAN_TYPES = (
        ('motorcycle_loan', 'Motorcycle Purchase Loan'),
        ('business_loan', 'Business Expansion Loan'),
        ('working_capital', 'Working Capital Loan'),
        ('asset_financing', 'Asset Financing'),
        ('refinancing', 'Loan Refinancing'),
    )
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('initial_review', 'Initial Review'),
        ('credit_assessment', 'Credit Assessment'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('conditional_approval', 'Conditional Approval'),
        ('documentation', 'Documentation Stage'),
        ('disbursed', 'Disbursed'),
    )
    
    # Basic Info
    application_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    applicant = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='bank_applications')
    bank = models.ForeignKey(BankProvider, on_delete=models.CASCADE, related_name='applications')
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
    
    # Loan Request Details
    requested_amount = models.DecimalField(max_digits=12, decimal_places=2)
    purpose = models.TextField()
    repayment_period_months = models.IntegerField()
    preferred_monthly_payment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Financial Information
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2)
    other_income = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    monthly_expenses = models.DecimalField(max_digits=10, decimal_places=2)
    existing_loans_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Employment/Business Details
    employment_type = models.CharField(max_length=50, default='Self-Employed')
    years_in_current_business = models.IntegerField()
    business_location = models.CharField(max_length=200)
    daily_revenue = models.DecimalField(max_digits=8, decimal_places=2)
    business_expenses_daily = models.DecimalField(max_digits=8, decimal_places=2)
    
    # Assets and Collateral
    owns_motorcycle = models.BooleanField(default=False)
    motorcycle_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    other_assets_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    collateral_offered = models.TextField(blank=True)
    
    # Banking History
    has_bank_account = models.BooleanField(default=True)
    bank_account_duration_months = models.IntegerField(default=0)
    credit_score = models.IntegerField(null=True, blank=True)
    previous_loan_history = models.TextField(blank=True)
    
    # References
    reference1_name = models.CharField(max_length=200)
    reference1_phone = models.CharField(max_length=20)
    reference1_relationship = models.CharField(max_length=100)
    
    reference2_name = models.CharField(max_length=200)
    reference2_phone = models.CharField(max_length=20)
    reference2_relationship = models.CharField(max_length=100)
    
    # Documentation Status
    documents_submitted = models.TextField(blank=True, help_text="List of submitted documents")
    documents_verified = models.BooleanField(default=False)
    additional_docs_required = models.TextField(blank=True)
    
    # Processing Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    submitted_at = models.DateTimeField(null=True, blank=True)
    bank_reference_number = models.CharField(max_length=50, blank=True)
    loan_officer_name = models.CharField(max_length=200, blank=True)
    loan_officer_phone = models.CharField(max_length=20, blank=True)
    
    # Bank Response
    bank_comments = models.TextField(blank=True)
    risk_assessment = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True)
    
    # Approval Details
    approved_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    approved_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    approved_term_months = models.IntegerField(null=True, blank=True)
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Conditions and Requirements
    approval_conditions = models.TextField(blank=True)
    insurance_required = models.BooleanField(default=False)
    guarantor_required = models.BooleanField(default=False)
    
    # Disbursement
    disbursement_date = models.DateField(null=True, blank=True)
    disbursement_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    loan_account_number = models.CharField(max_length=50, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Bank Loan Application"
        verbose_name_plural = "Bank Loan Applications"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.applicant.user.get_full_name()} - {self.bank.name} ({self.loan_type})"
    
    def get_debt_to_income_ratio(self):
        if self.monthly_income > 0:
            return (self.existing_loans_total / self.monthly_income) * 100
        return 0

class ApplicationDocument(models.Model):
    """
    Documents uploaded for SACCO or bank applications
    """
    DOCUMENT_TYPES = (
        ('national_id', 'National ID Copy'),
        ('kra_pin', 'KRA PIN Certificate'),
        ('passport_photo', 'Passport Photo'),
        ('bank_statements', 'Bank Statements (6 months)'),
        ('payslips', 'Payslips/Income Proof'),
        ('business_license', 'Business License'),
        ('logbook', 'Motorcycle Logbook'),
        ('insurance', 'Insurance Certificate'),
        ('guarantor_id', 'Guarantor ID Copy'),
        ('collateral_docs', 'Collateral Documents'),
        ('other', 'Other Documents'),
    )
    
    # Application References
    sacco_application = models.ForeignKey(SaccoApplication, on_delete=models.CASCADE, 
                                        related_name='documents', null=True, blank=True)
    bank_application = models.ForeignKey(BankLoanApplication, on_delete=models.CASCADE, 
                                       related_name='documents', null=True, blank=True)
    
    # Document Details
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    document_name = models.CharField(max_length=200)
    file = models.FileField(upload_to='application_documents/')
    file_size = models.IntegerField(help_text="File size in bytes")
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verified_by = models.CharField(max_length=200, blank=True)
    verification_notes = models.TextField(blank=True)
    
    # Metadata
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Application Document"
        verbose_name_plural = "Application Documents"
    
    def __str__(self):
        app_ref = self.sacco_application or self.bank_application
        return f"{self.document_name} - {app_ref}"

class LoanCalculation(models.Model):
    """
    Store loan calculations for users
    """
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='loan_calculations')
    provider_type = models.CharField(max_length=10, choices=[('sacco', 'SACCO'), ('bank', 'Bank')])
    provider_name = models.CharField(max_length=200)
    
    # Calculation Parameters
    principal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_months = models.IntegerField()
    
    # Results
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2)
    total_interest = models.DecimalField(max_digits=12, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Loan Calculation"
        verbose_name_plural = "Loan Calculations"
    
    def __str__(self):
        return f"{self.member.user.get_full_name()} - {self.provider_name} Calculation"
