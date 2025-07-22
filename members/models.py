from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

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
