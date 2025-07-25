from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class Member(models.Model):
    """
    Boda Boda rider member model
    Each rider registers with their details including ID, stage, zone, and next of kin
    """
    MEMBER_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('deceased', 'Deceased'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    national_id = models.CharField(max_length=20, unique=True, help_text="National ID Number")
    phone_number = models.CharField(
        max_length=15, 
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    stage = models.ForeignKey('stages.Stage', on_delete=models.CASCADE, related_name='members')
    zone = models.CharField(max_length=100, help_text="Area/Zone within the stage")
    sacco = models.CharField(max_length=200, blank=True, help_text="SACCO affiliation if any")
    
    # Next of kin information
    next_of_kin_name = models.CharField(max_length=200)
    next_of_kin_relationship = models.CharField(max_length=100)
    next_of_kin_phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    next_of_kin_id = models.CharField(max_length=20, help_text="Next of kin National ID")
    
    # Profile information
    profile_photo = models.ImageField(upload_to='member_photos/', blank=True, null=True)
    date_of_birth = models.DateField()
    address = models.TextField()
    
    # Membership details
    member_number = models.CharField(max_length=20, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=MEMBER_STATUS_CHOICES, default='active')
    
    # Online status tracking
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    # Dependents information
    dependents_count = models.PositiveIntegerField(default=0)
    dependents_details = models.JSONField(default=list, blank=True, help_text="List of dependents with their details")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['member_number']
        verbose_name = 'Member'
        verbose_name_plural = 'Members'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.member_number}"
    
    @property
    def full_name(self):
        return self.user.get_full_name()
    
    def total_contributions(self):
        """Calculate total contributions made by this member"""
        from contributions.models import Contribution
        return Contribution.objects.filter(member=self, status='completed').aggregate(
            total=models.Sum('amount')
        )['total'] or 0

class MemberDocument(models.Model):
    """
    Store member documents like ID copies, photos, etc.
    """
    DOCUMENT_TYPES = [
        ('national_id', 'National ID Copy'),
        ('passport_photo', 'Passport Photo'),
        ('next_of_kin_id', 'Next of Kin ID Copy'),
        ('birth_certificate', 'Birth Certificate'),
        ('other', 'Other Document'),
    ]
    
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    document_file = models.FileField(upload_to='member_documents/')
    description = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.member.user.get_full_name()} - {self.get_document_type_display()}"


class SaccoAffiliation(models.Model):
    """
    SACCO (Savings and Credit Cooperative) organizations that support boda boda riders
    """
    name = models.CharField(max_length=200, unique=True)
    coverage_area = models.CharField(max_length=100, help_text="Geographic coverage area")
    description = models.TextField(blank=True, help_text="Description of SACCO services")
    supports_bodaboda = models.BooleanField(default=True, help_text="Whether this SACCO specifically supports boda boda riders")
    is_active = models.BooleanField(default=True)
    
    # Contact information
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    physical_address = models.TextField(blank=True)
    
    # Services offered
    offers_motorcycle_loans = models.BooleanField(default=False)
    offers_insurance = models.BooleanField(default=False)
    offers_savings_accounts = models.BooleanField(default=False)
    offers_emergency_fund = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "SACCO Affiliation"
        verbose_name_plural = "SACCO Affiliations"
    
    def __str__(self):
        return self.name


class MemberProfile(models.Model):
    """
    Extended profile for member users with admin capabilities and king cap indicator
    """
    ACCOUNT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]
    
    COMPLETION_STATUS_CHOICES = [
        ('incomplete', 'Incomplete'),
        ('pending_verification', 'Pending Verification'),
        ('complete', 'Complete'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='memberprofile')
    phone_number = models.CharField(max_length=15, blank=True)
    national_id = models.CharField(max_length=20, blank=True)
    bike_registration = models.CharField(max_length=50, blank=True)
    stage = models.ForeignKey('stages.Stage', on_delete=models.SET_NULL, null=True, blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    emergency_contact_relationship = models.CharField(max_length=100, blank=True)
    next_of_kin = models.CharField(max_length=200, blank=True)
    next_of_kin_contact = models.CharField(max_length=15, blank=True)
    
    # Admin privileges
    is_admin = models.BooleanField(default=False, help_text="👑 Admin user with elevated privileges")
    is_super_admin = models.BooleanField(default=False, help_text="👑 Super admin with full system access")
    
    # Profile status
    account_status = models.CharField(max_length=20, choices=ACCOUNT_STATUS_CHOICES, default='pending')
    profile_completion_status = models.CharField(max_length=20, choices=COMPLETION_STATUS_CHOICES, default='incomplete')
    
    # Profile photo
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Member Profile'
        verbose_name_plural = 'Member Profiles'
    
    def __str__(self):
        crown = "👑 " if self.is_super_admin else "🛡️ " if self.is_admin else ""
        return f"{crown}{self.user.get_full_name() or self.user.username}"
    
    @property
    def display_name_with_crown(self):
        """Return display name with crown indicator for admin users"""
        crown = "👑 " if self.is_super_admin else "🛡️ " if self.is_admin else ""
        return f"{crown}{self.user.get_full_name() or self.user.username}"
    
    def delete(self, *args, **kwargs):
        """Prevent deletion of super admin profiles"""
        if self.is_super_admin:
            raise ValidationError("👑 Super admin profiles cannot be deleted for system security.")
        return super().delete(*args, **kwargs)
