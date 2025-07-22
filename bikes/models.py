from django.db import models

class Bike(models.Model):
    """
    Bike ownership records to help families recover assets
    """
    BIKE_STATUS = [
        ('active', 'Active/In Use'),
        ('repair', 'Under Repair'),
        ('stolen', 'Stolen'),
        ('sold', 'Sold'),
        ('written_off', 'Written Off'),
        ('inherited', 'Inherited by Family'),
    ]
    
    owner = models.ForeignKey('members.Member', on_delete=models.CASCADE, related_name='bikes')
    
    # Bike identification
    registration_number = models.CharField(max_length=20, unique=True)
    chassis_number = models.CharField(max_length=50, unique=True)
    engine_number = models.CharField(max_length=50)
    
    # Bike details
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year_of_manufacture = models.PositiveIntegerField()
    color = models.CharField(max_length=50)
    cc = models.PositiveIntegerField(help_text="Engine capacity in CC")
    
    # Ownership details
    purchase_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Current estimated value")
    
    # Documentation
    logbook_available = models.BooleanField(default=True)
    logbook_location = models.CharField(max_length=200, blank=True, help_text="Where logbook is kept")
    insurance_policy_number = models.CharField(max_length=100, blank=True)
    insurance_company = models.CharField(max_length=200, blank=True)
    insurance_expiry = models.DateField(null=True, blank=True)
    
    # Status and condition
    status = models.CharField(max_length=20, choices=BIKE_STATUS, default='active')
    condition_notes = models.TextField(blank=True)
    
    # Family access information
    family_contact_informed = models.BooleanField(default=False)
    next_of_kin_has_access = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['registration_number']
        verbose_name = 'Bike'
        verbose_name_plural = 'Bikes'
    
    def __str__(self):
        return f"{self.registration_number} - {self.make} {self.model} ({self.owner.full_name})"

class BikeDocument(models.Model):
    """
    Store bike-related documents
    """
    DOCUMENT_TYPES = [
        ('logbook', 'Logbook'),
        ('insurance_certificate', 'Insurance Certificate'),
        ('purchase_receipt', 'Purchase Receipt'),
        ('inspection_certificate', 'Inspection Certificate'),
        ('registration_certificate', 'Registration Certificate'),
        ('photo', 'Bike Photo'),
        ('other', 'Other Document'),
    ]
    
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPES)
    document_file = models.FileField(upload_to='bike_documents/')
    description = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.bike.registration_number} - {self.get_document_type_display()}"

class BikeTransfer(models.Model):
    """
    Track bike ownership transfers (inheritance, sale, etc.)
    """
    TRANSFER_TYPES = [
        ('inheritance', 'Inheritance'),
        ('sale', 'Sale'),
        ('gift', 'Gift'),
        ('recovery', 'Recovery from Theft'),
        ('insurance_claim', 'Insurance Claim'),
    ]
    
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, related_name='transfers')
    transfer_type = models.CharField(max_length=20, choices=TRANSFER_TYPES)
    
    # Transfer details
    from_member = models.ForeignKey(
        'members.Member', 
        on_delete=models.CASCADE, 
        related_name='bikes_transferred_from'
    )
    to_member = models.ForeignKey(
        'members.Member', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='bikes_transferred_to'
    )
    to_family_member = models.CharField(max_length=200, blank=True, help_text="If transferred to non-member family")
    
    # Transfer conditions
    transfer_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    transfer_date = models.DateField()
    conditions = models.TextField(blank=True)
    
    # Documentation
    witnessed_by = models.ForeignKey(
        'members.Member', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='witnessed_transfers'
    )
    transfer_document = models.FileField(upload_to='transfer_documents/', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-transfer_date']
    
    def __str__(self):
        return f"{self.bike.registration_number} - {self.get_transfer_type_display()}"
