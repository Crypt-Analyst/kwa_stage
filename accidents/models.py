from django.db import models

class AccidentReport(models.Model):
    """
    Quick accident reporting system to alert SACCO and other riders
    """
    ACCIDENT_SEVERITY = [
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
        ('fatal', 'Fatal'),
    ]
    
    ACCIDENT_STATUS = [
        ('reported', 'Just Reported'),
        ('help_dispatched', 'Help Dispatched'),
        ('hospital', 'Taken to Hospital'),
        ('resolved', 'Resolved'),
        ('follow_up', 'Follow-up Required'),
    ]
    
    report_number = models.CharField(max_length=20, unique=True)
    member = models.ForeignKey('members.Member', on_delete=models.CASCADE, related_name='accident_reports')
    
    # Accident details
    accident_date = models.DateTimeField()
    location = models.CharField(max_length=300)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=ACCIDENT_SEVERITY)
    status = models.CharField(max_length=20, choices=ACCIDENT_STATUS, default='reported')
    
    # Parties involved
    other_parties_involved = models.TextField(blank=True, help_text="Other vehicles, people involved")
    police_involved = models.BooleanField(default=False)
    police_station = models.CharField(max_length=200, blank=True)
    ob_number = models.CharField(max_length=50, blank=True, help_text="Police OB Number")
    
    # Medical information
    injuries_sustained = models.TextField(blank=True)
    hospital_taken_to = models.CharField(max_length=200, blank=True)
    medical_expenses = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Bike damage
    bike_damaged = models.BooleanField(default=False)
    bike_damage_description = models.TextField(blank=True)
    estimated_repair_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Reporting and response
    reported_by = models.ForeignKey(
        'members.Member', 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='reported_accidents'
    )
    first_responders = models.ManyToManyField(
        'members.Member',
        blank=True,
        related_name='responded_accidents'
    )
    
    # Follow-up
    insurance_claimed = models.BooleanField(default=False)
    insurance_company = models.CharField(max_length=200, blank=True)
    claim_reference = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-accident_date']
        verbose_name = 'Accident Report'
        verbose_name_plural = 'Accident Reports'
    
    def __str__(self):
        return f"{self.report_number} - {self.member.full_name} ({self.get_severity_display()})"

class AccidentAlert(models.Model):
    """
    SMS/notification alerts sent for accidents
    """
    ALERT_TYPES = [
        ('sms', 'SMS Alert'),
        ('call', 'Phone Call'),
        ('whatsapp', 'WhatsApp Message'),
        ('system', 'System Notification'),
    ]
    
    accident_report = models.ForeignKey(AccidentReport, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    
    # Recipients
    recipient_member = models.ForeignKey('members.Member', on_delete=models.CASCADE, null=True, blank=True)
    recipient_phone = models.CharField(max_length=15)
    recipient_name = models.CharField(max_length=200)
    
    # Alert content
    message = models.TextField()
    sent_successfully = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"{self.get_alert_type_display()} to {self.recipient_name}"
