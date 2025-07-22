from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .constants import KENYAN_COUNTIES, MAJOR_TOWNS

class Organization(models.Model):
    """
    Main organization/SACCO that can have multiple stages and chamas
    """
    ORGANIZATION_TYPES = [
        ('sacco', 'SACCO'),
        ('chama', 'Chama'),
        ('stage_group', 'Stage Group'),
        ('welfare_society', 'Welfare Society'),
    ]
    
    name = models.CharField(max_length=200, unique=True)
    organization_type = models.CharField(max_length=20, choices=ORGANIZATION_TYPES)
    registration_number = models.CharField(max_length=100, unique=True, help_text="Official registration number")
    description = models.TextField(blank=True)
    
    # Contact information
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    email = models.EmailField()
    website = models.URLField(blank=True)
    
    # Address
    county = models.CharField(max_length=100, choices=KENYAN_COUNTIES)
    sub_county = models.CharField(max_length=100)
    town = models.CharField(max_length=100, choices=MAJOR_TOWNS)
    address = models.TextField()
    
    # Admin details
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='administered_organizations')
    
    # Settings
    is_active = models.BooleanField(default=True)
    allow_inter_org_communication = models.BooleanField(default=True, help_text="Allow communication with other organizations for lost bikes etc")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
    
    def __str__(self):
        return f"{self.name} ({self.get_organization_type_display()})"
    
    def total_members(self):
        """Total members across all stages in this organization"""
        return sum(stage.active_members_count() for stage in self.stages.all())
    
    def total_stages(self):
        """Total stages in this organization"""
        return self.stages.filter(is_active=True).count()

class Chama(models.Model):
    """
    Sub-groups within an organization for specific purposes
    """
    CHAMA_TYPES = [
        ('welfare', 'Welfare Fund'),
        ('investment', 'Investment Group'),
        ('savings', 'Savings Group'),
        ('emergency', 'Emergency Fund'),
        ('loan', 'Loan Group'),
    ]
    
    name = models.CharField(max_length=200)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='chamas')
    chama_type = models.CharField(max_length=20, choices=CHAMA_TYPES)
    description = models.TextField(blank=True)
    
    # Chama leadership
    chairman = models.ForeignKey(
        'members.Member', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='chaired_chamas'
    )
    secretary = models.ForeignKey(
        'members.Member', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='secretary_chamas'
    )
    treasurer = models.ForeignKey(
        'members.Member', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='treasurer_chamas'
    )
    
    # Settings
    minimum_contribution = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    meeting_day = models.CharField(max_length=20, blank=True, help_text="e.g., Every Friday")
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        unique_together = ['organization', 'name']
        verbose_name = 'Chama'
        verbose_name_plural = 'Chamas'
    
    def __str__(self):
        return f"{self.name} - {self.organization.name}"
    
    def members_count(self):
        """Count of active members in this chama"""
        return self.memberships.filter(is_active=True).count()

class Stage(models.Model):
    """
    Boda Boda stages/stations where riders operate
    """
    name = models.CharField(max_length=200)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='stages')
    location = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    
    # Geographic coordinates
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, help_text="GPS Latitude coordinate")
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, help_text="GPS Longitude coordinate")
    
    # Stage leadership
    stage_leader = models.ForeignKey(
        'members.Member', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='led_stages'
    )
    
    # Contact information
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    
    # Location details
    county = models.CharField(max_length=100, choices=KENYAN_COUNTIES)
    sub_county = models.CharField(max_length=100)
    ward = models.CharField(max_length=100)
    
    # Stage details
    registration_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        unique_together = ['organization', 'name']
        verbose_name = 'Stage'
        verbose_name_plural = 'Stages'
    
    def __str__(self):
        return f"{self.name} - {self.organization.name}"
    
    def active_members_count(self):
        """Count of active members in this stage"""
        return self.members.filter(status='active').count()
    
    def total_contributions(self):
        """Total contributions from all members in this stage"""
        from contributions.models import Contribution
        return Contribution.objects.filter(
            member__stage=self, 
            status='completed'
        ).aggregate(total=models.Sum('amount'))['total'] or 0

class StageLeadership(models.Model):
    """
    Track stage leadership history and roles
    """
    LEADERSHIP_ROLES = [
        ('chairman', 'Chairman'),
        ('secretary', 'Secretary'),
        ('treasurer', 'Treasurer'),
        ('organizer', 'Organizer'),
        ('coordinator', 'Coordinator'),
    ]
    
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='leadership_history')
    member = models.ForeignKey('members.Member', on_delete=models.CASCADE, related_name='leadership_roles')
    role = models.CharField(max_length=20, choices=LEADERSHIP_ROLES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_date']
        unique_together = ['stage', 'role', 'is_current']
    
    def __str__(self):
        return f"{self.member.full_name} - {self.get_role_display()} at {self.stage.name}"

class ChamaMembership(models.Model):
    """
    Track which members belong to which chamas
    """
    chama = models.ForeignKey(Chama, on_delete=models.CASCADE, related_name='memberships')
    member = models.ForeignKey('members.Member', on_delete=models.CASCADE, related_name='chama_memberships')
    joined_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    # Membership details
    monthly_contribution = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['chama', 'member']
        ordering = ['-joined_date']
    
    def __str__(self):
        return f"{self.member.full_name} - {self.chama.name}"

class InterOrgCommunication(models.Model):
    """
    Communication platform for inter-organization communication
    Like a WhatsApp group for lost bikes and announcements
    """
    COMMUNICATION_TYPES = [
        ('lost_bike', 'Lost Bike Alert'),
        ('found_bike', 'Found Bike Report'),
        ('emergency', 'Emergency Alert'),
        ('announcement', 'General Announcement'),
        ('meeting', 'Meeting Notice'),
    ]
    
    sender_organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='sent_communications')
    sender_member = models.ForeignKey('members.Member', on_delete=models.CASCADE, related_name='sent_communications')
    
    communication_type = models.CharField(max_length=20, choices=COMMUNICATION_TYPES)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    # For lost bike alerts
    bike_registration = models.CharField(max_length=50, blank=True, help_text="Bike registration number if applicable")
    location_lost = models.CharField(max_length=200, blank=True, help_text="Location where bike was lost")
    contact_phone = models.CharField(max_length=15, blank=True)
    
    # Attachments
    image = models.ImageField(upload_to='inter_org_communications/', blank=True, null=True)
    
    # Delivery
    is_broadcast = models.BooleanField(default=True, help_text="Send to all organizations or specific ones")
    target_organizations = models.ManyToManyField(Organization, blank=True, related_name='received_communications')
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False, help_text="Mark as resolved for lost bike cases")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Inter-Organization Communication'
        verbose_name_plural = 'Inter-Organization Communications'
    
    def __str__(self):
        return f"{self.get_communication_type_display()}: {self.subject}"
