from django.db import models
from decimal import Decimal

class EmergencyCase(models.Model):
    """
    Track emergency cases (death, accidents, family support)
    """
    CASE_TYPES = [
        ('death', 'Death'),
        ('accident', 'Accident'),
        ('illness', 'Serious Illness'),
        ('family_emergency', 'Family Emergency'),
        ('fire', 'Fire Incident'),
        ('theft', 'Theft/Robbery'),
    ]
    
    CASE_STATUS = [
        ('reported', 'Reported'),
        ('verified', 'Verified'),
        ('approved', 'Approved'),
        ('disbursed', 'Funds Disbursed'),
        ('closed', 'Case Closed'),
        ('rejected', 'Rejected'),
    ]
    
    case_number = models.CharField(max_length=20, unique=True)
    member = models.ForeignKey('members.Member', on_delete=models.CASCADE, related_name='emergency_cases')
    case_type = models.CharField(max_length=20, choices=CASE_TYPES)
    status = models.CharField(max_length=20, choices=CASE_STATUS, default='reported')
    
    # Case details
    incident_date = models.DateField()
    description = models.TextField()
    location = models.CharField(max_length=300)
    
    # Financial details
    requested_amount = models.DecimalField(max_digits=10, decimal_places=2)
    approved_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    disbursed_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Family/beneficiary information
    beneficiary_name = models.CharField(max_length=200)
    beneficiary_relationship = models.CharField(max_length=100)
    beneficiary_phone = models.CharField(max_length=15)
    beneficiary_id = models.CharField(max_length=20)
    
    # Case handling
    reported_by = models.ForeignKey(
        'members.Member', 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='reported_emergencies'
    )
    verified_by = models.ForeignKey(
        'members.Member', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='verified_emergencies'
    )
    approved_by = models.ForeignKey(
        'members.Member', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='approved_emergencies'
    )
    
    # Important dates
    verification_date = models.DateTimeField(null=True, blank=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    disbursement_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Emergency Case'
        verbose_name_plural = 'Emergency Cases'
    
    def __str__(self):
        return f"{self.case_number} - {self.member.full_name} ({self.get_case_type_display()})"

class FamilySupportRecord(models.Model):
    """
    Track family support provided and dependents helped
    """
    emergency_case = models.ForeignKey(EmergencyCase, on_delete=models.CASCADE, related_name='support_records')
    
    # Support details
    support_type = models.CharField(max_length=100, help_text="Type of support provided")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    recipient_name = models.CharField(max_length=200)
    recipient_relationship = models.CharField(max_length=100)
    
    # Dependent information
    dependents_count = models.PositiveIntegerField(default=0)
    dependents_ages = models.JSONField(default=list, help_text="List of dependent ages")
    
    # Support tracking
    payment_method = models.CharField(max_length=50)
    transaction_reference = models.CharField(max_length=100, blank=True)
    
    provided_by = models.ForeignKey('members.Member', on_delete=models.SET_NULL, null=True)
    provided_date = models.DateTimeField(auto_now_add=True)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-provided_date']
    
    def __str__(self):
        return f"Support for {self.recipient_name} - KSh {self.amount}"
