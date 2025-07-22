from django.db import models
from django.contrib.auth.models import User
from members.models import Member

class Insurance(models.Model):
    """
    Insurance policies for bikes and members
    """
    INSURANCE_TYPES = [
        ('bike_comprehensive', 'Bike Comprehensive'),
        ('bike_third_party', 'Bike Third Party'),
        ('personal_accident', 'Personal Accident'),
        ('medical', 'Medical Insurance'),
        ('life', 'Life Insurance'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending Renewal'),
    ]
    
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='insurances')
    bike = models.ForeignKey('bikes.Bike', on_delete=models.CASCADE, blank=True, null=True)
    
    insurance_type = models.CharField(max_length=20, choices=INSURANCE_TYPES)
    policy_number = models.CharField(max_length=100, unique=True)
    insurance_company = models.CharField(max_length=200)
    
    # Policy details
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Dates
    start_date = models.DateField()
    end_date = models.DateField()
    reminder_date = models.DateField(help_text="Date to send renewal reminder")
    
    # Status and documents
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    policy_document = models.FileField(upload_to='insurance_documents/', blank=True)
    
    # Contact and claims
    agent_name = models.CharField(max_length=200, blank=True)
    agent_phone = models.CharField(max_length=20, blank=True)
    claims_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-end_date']
    
    def __str__(self):
        return f"{self.get_insurance_type_display()} - {self.policy_number}"
    
    @property
    def is_expiring_soon(self):
        from datetime import date, timedelta
        return self.end_date <= date.today() + timedelta(days=30)
    
    @property
    def is_expired(self):
        from datetime import date
        return self.end_date < date.today()

class License(models.Model):
    """
    Driving licenses and permits for members
    """
    LICENSE_TYPES = [
        ('driving_license', 'Driving License'),
        ('motorcycle_permit', 'Motorcycle Permit'),
        ('commercial_permit', 'Commercial Permit'),
        ('psv_license', 'PSV License'),
        ('good_conduct', 'Certificate of Good Conduct'),
    ]
    
    STATUS_CHOICES = [
        ('valid', 'Valid'),
        ('expired', 'Expired'),
        ('suspended', 'Suspended'),
        ('revoked', 'Revoked'),
        ('pending_renewal', 'Pending Renewal'),
    ]
    
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='licenses')
    
    license_type = models.CharField(max_length=20, choices=LICENSE_TYPES)
    license_number = models.CharField(max_length=100, unique=True)
    
    # Dates
    issue_date = models.DateField()
    expiry_date = models.DateField()
    reminder_date = models.DateField(help_text="Date to send renewal reminder")
    
    # Status and documents
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='valid')
    issuing_authority = models.CharField(max_length=200)
    license_document = models.FileField(upload_to='license_documents/', blank=True)
    
    # Additional info
    restrictions = models.TextField(blank=True, help_text="Any restrictions on the license")
    endorsements = models.TextField(blank=True, help_text="Special endorsements")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-expiry_date']
    
    def __str__(self):
        return f"{self.get_license_type_display()} - {self.license_number}"
    
    @property
    def is_expiring_soon(self):
        from datetime import date, timedelta
        return self.expiry_date <= date.today() + timedelta(days=30)
    
    @property
    def is_expired(self):
        from datetime import date
        return self.expiry_date < date.today()

class SafetyTraining(models.Model):
    """
    Safety training records for members
    """
    TRAINING_TYPES = [
        ('defensive_driving', 'Defensive Driving'),
        ('first_aid', 'First Aid'),
        ('motorcycle_safety', 'Motorcycle Safety'),
        ('traffic_rules', 'Traffic Rules & Regulations'),
        ('emergency_response', 'Emergency Response'),
        ('customer_service', 'Customer Service'),
        ('road_safety', 'Road Safety'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('missed', 'Missed'),
        ('cancelled', 'Cancelled'),
        ('in_progress', 'In Progress'),
    ]
    
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='safety_trainings')
    
    training_type = models.CharField(max_length=20, choices=TRAINING_TYPES)
    training_title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Training details
    trainer_name = models.CharField(max_length=200)
    training_institution = models.CharField(max_length=200)
    venue = models.CharField(max_length=200)
    
    # Dates and duration
    scheduled_date = models.DateTimeField()
    completed_date = models.DateTimeField(blank=True, null=True)
    duration_hours = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Status and results
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, 
                               help_text="Training score (if applicable)")
    passed = models.BooleanField(default=False)
    
    # Documents
    certificate = models.FileField(upload_to='training_certificates/', blank=True)
    attendance_sheet = models.FileField(upload_to='training_attendance/', blank=True)
    
    # Renewal info
    certificate_expiry = models.DateField(blank=True, null=True)
    renewal_required = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_date']
    
    def __str__(self):
        return f"{self.training_title} - {self.member.user.get_full_name()}"
    
    @property
    def is_certificate_expiring(self):
        if not self.certificate_expiry:
            return False
        from datetime import date, timedelta
        return self.certificate_expiry <= date.today() + timedelta(days=30)

class ComplianceChecklist(models.Model):
    """
    Compliance checklist for members to track required documents and training
    """
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='compliance')
    
    # Insurance compliance
    bike_insurance_valid = models.BooleanField(default=False)
    personal_insurance_valid = models.BooleanField(default=False)
    
    # License compliance
    driving_license_valid = models.BooleanField(default=False)
    motorcycle_permit_valid = models.BooleanField(default=False)
    commercial_permit_valid = models.BooleanField(default=False)
    
    # Training compliance
    safety_training_completed = models.BooleanField(default=False)
    first_aid_training_completed = models.BooleanField(default=False)
    
    # Additional requirements
    good_conduct_certificate = models.BooleanField(default=False)
    stage_membership_active = models.BooleanField(default=True)
    
    # Overall compliance
    compliance_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    last_updated = models.DateTimeField(auto_now=True)
    
    def calculate_compliance_score(self):
        """Calculate overall compliance percentage"""
        total_fields = 8  # Total number of compliance fields
        completed_fields = sum([
            self.bike_insurance_valid,
            self.personal_insurance_valid,
            self.driving_license_valid,
            self.motorcycle_permit_valid,
            self.commercial_permit_valid,
            self.safety_training_completed,
            self.first_aid_training_completed,
            self.good_conduct_certificate,
        ])
        self.compliance_score = (completed_fields / total_fields) * 100
        self.save()
        return self.compliance_score
    
    def __str__(self):
        return f"Compliance - {self.member.user.get_full_name()} ({self.compliance_score}%)"

class SafetyIncident(models.Model):
    """
    Record safety incidents and near misses
    """
    INCIDENT_TYPES = [
        ('accident', 'Accident'),
        ('near_miss', 'Near Miss'),
        ('equipment_failure', 'Equipment Failure'),
        ('unsafe_behavior', 'Unsafe Behavior'),
        ('harassment', 'Harassment'),
        ('theft', 'Theft/Robbery'),
    ]
    
    SEVERITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    reporter = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='reported_incidents')
    involved_member = models.ForeignKey(Member, on_delete=models.CASCADE, blank=True, null=True,
                                       related_name='involved_incidents')
    
    incident_type = models.CharField(max_length=20, choices=INCIDENT_TYPES)
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS)
    
    # Incident details
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=300)
    incident_date = models.DateTimeField()
    
    # Follow-up actions
    action_taken = models.TextField(blank=True)
    preventive_measures = models.TextField(blank=True)
    investigation_required = models.BooleanField(default=False)
    investigation_completed = models.BooleanField(default=False)
    
    # Status
    is_resolved = models.BooleanField(default=False)
    resolution_date = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-incident_date']
    
    def __str__(self):
        return f"{self.title} - {self.get_severity_display()}"
