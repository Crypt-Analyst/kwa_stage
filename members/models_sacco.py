"""
SACCO Models for Kenya Boda Boda Welfare System
Comprehensive list of SACCOs in Kenya that support boda boda riders
"""
from django.db import models
from django.contrib.auth.models import User

class SaccoCategory(models.Model):
    """Categories of SACCOs"""
    CATEGORY_CHOICES = [
        ('transport', 'Transport & Motorbike SACCOs'),
        ('farmers', 'Farmers SACCOs'),
        ('teachers', 'Teachers SACCOs'),
        ('deposit_taking', 'Deposit Taking SACCOs (DT-SACCOs)'),
        ('credit_only', 'Credit Only SACCOs'),
        ('multi_purpose', 'Multi-Purpose SACCOs'),
        ('youth', 'Youth SACCOs'),
        ('women', 'Women SACCOs'),
        ('community', 'Community Based SACCOs'),
        ('church', 'Church/Religious SACCOs'),
        ('professional', 'Professional SACCOs'),
        ('county', 'County Government SACCOs'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    supports_boda_boda = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "SACCO Category"
        verbose_name_plural = "SACCO Categories"
    
    def __str__(self):
        return self.name

class County(models.Model):
    """Kenya Counties"""
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True)
    region = models.CharField(max_length=50)  # Central, Coast, Eastern, etc.
    
    class Meta:
        verbose_name_plural = "Counties"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class SaccoAffiliation(models.Model):
    """Comprehensive SACCO data for Kenya"""
    name = models.CharField(max_length=200, unique=True)
    acronym = models.CharField(max_length=20, blank=True, help_text="SACCO acronym/short name")
    category = models.ForeignKey(SaccoCategory, on_delete=models.CASCADE)
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    town = models.CharField(max_length=100, blank=True)
    
    # Contact Information
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    physical_address = models.TextField(blank=True)
    
    # Registration & Licensing
    license_number = models.CharField(max_length=50, blank=True)
    registration_date = models.DateField(null=True, blank=True)
    is_licensed = models.BooleanField(default=True)
    regulatory_body = models.CharField(max_length=100, default="SASRA")  # SASRA, Ministry of Cooperatives
    
    # Services
    supports_boda_boda = models.BooleanField(default=False, help_text="Specifically serves boda boda riders")
    offers_loans = models.BooleanField(default=True)
    offers_savings = models.BooleanField(default=True)
    offers_insurance = models.BooleanField(default=False)
    offers_mobile_banking = models.BooleanField(default=False)
    minimum_share_capital = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Membership
    total_members = models.IntegerField(null=True, blank=True)
    boda_boda_members = models.IntegerField(null=True, blank=True)
    
    # Financial Information
    total_assets = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    loan_portfolio = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_recommended = models.BooleanField(default=False, help_text="Recommended for boda boda riders")
    notes = models.TextField(blank=True, help_text="Special notes about this SACCO")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "SACCO Affiliation"
        verbose_name_plural = "SACCO Affiliations"
        ordering = ['name']
        indexes = [
            models.Index(fields=['county', 'category']),
            models.Index(fields=['supports_boda_boda']),
            models.Index(fields=['is_active', 'is_recommended']),
        ]
    
    def __str__(self):
        if self.acronym:
            return f"{self.name} ({self.acronym})"
        return self.name
    
    @property
    def display_name(self):
        """Display name for dropdowns"""
        location = f"{self.town}, {self.county.name}" if self.town else self.county.name
        return f"{self.name} - {location}"
    
    @property
    def is_deposit_taking(self):
        """Check if this is a Deposit Taking SACCO"""
        return self.category.category == 'deposit_taking'
    
    def get_services_list(self):
        """Get list of services offered"""
        services = []
        if self.offers_loans:
            services.append("Loans")
        if self.offers_savings:
            services.append("Savings")
        if self.offers_insurance:
            services.append("Insurance")
        if self.offers_mobile_banking:
            services.append("Mobile Banking")
        return services

class MemberSaccoHistory(models.Model):
    """Track member's SACCO affiliation history"""
    from .models import Member
    
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='sacco_history')
    sacco = models.ForeignKey(SaccoAffiliation, on_delete=models.CASCADE)
    membership_number = models.CharField(max_length=50, blank=True)
    date_joined = models.DateField()
    date_left = models.DateField(null=True, blank=True)
    reason_for_leaving = models.TextField(blank=True)
    is_current = models.BooleanField(default=True)
    
    # Financial details
    share_capital_contributed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_savings = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    outstanding_loans = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Member SACCO History"
        verbose_name_plural = "Member SACCO Histories"
        ordering = ['-date_joined']
        unique_together = ['member', 'sacco', 'date_joined']
    
    def __str__(self):
        status = "Current" if self.is_current else "Former"
        return f"{self.member.user.get_full_name()} - {self.sacco.name} ({status})"
