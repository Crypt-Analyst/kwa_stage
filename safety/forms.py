from django import forms
from django.core.exceptions import ValidationError
from datetime import date, timedelta

from .models import Insurance, License, SafetyTraining, SafetyIncident


class InsuranceForm(forms.ModelForm):
    """
    Form for adding/editing insurance policies
    """
    
    class Meta:
        model = Insurance
        fields = [
            'insurance_type', 'policy_number', 'insurance_company',
            'coverage_amount', 'premium_amount', 'start_date', 'end_date',
            'reminder_date', 'policy_document', 'agent_name', 'agent_phone'
        ]
        widgets = {
            'insurance_type': forms.Select(attrs={'class': 'form-control'}),
            'policy_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter policy number'}),
            'insurance_company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter insurance company name'}),
            'coverage_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'premium_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reminder_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'policy_document': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.jpg,.jpeg,.png'}),
            'agent_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Agent name (optional)'}),
            'agent_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Agent phone (optional)'}),
        }
        labels = {
            'insurance_type': 'Insurance Type',
            'policy_number': 'Policy Number',
            'insurance_company': 'Insurance Company',
            'coverage_amount': 'Coverage Amount (KES)',
            'premium_amount': 'Premium Amount (KES)',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'reminder_date': 'Renewal Reminder Date',
            'policy_document': 'Policy Document',
            'agent_name': 'Agent Name',
            'agent_phone': 'Agent Phone',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        reminder_date = cleaned_data.get('reminder_date')
        
        if start_date and end_date:
            if start_date >= end_date:
                raise ValidationError("End date must be after start date.")
        
        if reminder_date and end_date:
            if reminder_date >= end_date:
                raise ValidationError("Reminder date must be before end date.")
        
        return cleaned_data
    
    def clean_policy_number(self):
        policy_number = self.cleaned_data.get('policy_number')
        if policy_number:
            # Check for duplicate policy numbers (excluding current instance if editing)
            existing = Insurance.objects.filter(policy_number=policy_number)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError("A policy with this number already exists.")
        return policy_number


class LicenseForm(forms.ModelForm):
    """
    Form for adding/editing licenses and permits
    """
    
    class Meta:
        model = License
        fields = [
            'license_type', 'license_number', 'issue_date', 'expiry_date',
            'reminder_date', 'issuing_authority', 'license_document',
            'restrictions', 'endorsements'
        ]
        widgets = {
            'license_type': forms.Select(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter license number'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reminder_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'issuing_authority': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., NTSA, DCI'}),
            'license_document': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.jpg,.jpeg,.png'}),
            'restrictions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any restrictions (optional)'}),
            'endorsements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Special endorsements (optional)'}),
        }
        labels = {
            'license_type': 'License/Permit Type',
            'license_number': 'License/Permit Number',
            'issue_date': 'Issue Date',
            'expiry_date': 'Expiry Date',
            'reminder_date': 'Renewal Reminder Date',
            'issuing_authority': 'Issuing Authority',
            'license_document': 'License Document',
            'restrictions': 'Restrictions',
            'endorsements': 'Endorsements',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        issue_date = cleaned_data.get('issue_date')
        expiry_date = cleaned_data.get('expiry_date')
        reminder_date = cleaned_data.get('reminder_date')
        
        if issue_date and expiry_date:
            if issue_date >= expiry_date:
                raise ValidationError("Expiry date must be after issue date.")
        
        if reminder_date and expiry_date:
            if reminder_date >= expiry_date:
                raise ValidationError("Reminder date must be before expiry date.")
        
        return cleaned_data
    
    def clean_license_number(self):
        license_number = self.cleaned_data.get('license_number')
        if license_number:
            # Check for duplicate license numbers (excluding current instance if editing)
            existing = License.objects.filter(license_number=license_number)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError("A license with this number already exists.")
        return license_number


class SafetyTrainingForm(forms.ModelForm):
    """
    Form for adding/editing safety training records
    """
    
    class Meta:
        model = SafetyTraining
        fields = [
            'training_type', 'training_title', 'description', 'trainer_name',
            'training_institution', 'venue', 'scheduled_date', 'duration_hours',
            'status', 'score', 'passed', 'certificate', 'certificate_expiry',
            'renewal_required'
        ]
        widgets = {
            'training_type': forms.Select(attrs={'class': 'form-control'}),
            'training_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter training title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Training description'}),
            'trainer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Trainer name'}),
            'training_institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Training institution'}),
            'venue': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Training venue'}),
            'scheduled_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'duration_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0.5'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'passed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'certificate': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.jpg,.jpeg,.png'}),
            'certificate_expiry': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'renewal_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'training_type': 'Training Type',
            'training_title': 'Training Title',
            'description': 'Description',
            'trainer_name': 'Trainer Name',
            'training_institution': 'Training Institution',
            'venue': 'Venue',
            'scheduled_date': 'Scheduled Date & Time',
            'duration_hours': 'Duration (Hours)',
            'status': 'Status',
            'score': 'Score (%)',
            'passed': 'Passed',
            'certificate': 'Certificate',
            'certificate_expiry': 'Certificate Expiry Date',
            'renewal_required': 'Renewal Required',
        }
    
    def clean_score(self):
        score = self.cleaned_data.get('score')
        if score is not None and (score < 0 or score > 100):
            raise ValidationError("Score must be between 0 and 100.")
        return score


class SafetyIncidentForm(forms.ModelForm):
    """
    Form for reporting safety incidents
    """
    
    class Meta:
        model = SafetyIncident
        fields = [
            'incident_type', 'severity', 'title', 'description', 'location',
            'incident_date', 'involved_member', 'action_taken', 'preventive_measures',
            'investigation_required'
        ]
        widgets = {
            'incident_type': forms.Select(attrs={'class': 'form-control'}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief incident title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Detailed description of the incident'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Where did the incident occur?'}),
            'incident_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'involved_member': forms.Select(attrs={'class': 'form-control'}),
            'action_taken': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'What immediate actions were taken? (optional)'}),
            'preventive_measures': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Suggested preventive measures (optional)'}),
            'investigation_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'incident_type': 'Incident Type',
            'severity': 'Severity Level',
            'title': 'Incident Title',
            'description': 'Description',
            'location': 'Location',
            'incident_date': 'Incident Date & Time',
            'involved_member': 'Involved Member (if applicable)',
            'action_taken': 'Immediate Action Taken',
            'preventive_measures': 'Preventive Measures',
            'investigation_required': 'Investigation Required',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set involved_member queryset to all members
        from members.models import Member
        self.fields['involved_member'].queryset = Member.objects.all()
        self.fields['involved_member'].required = False
    
    def clean_incident_date(self):
        incident_date = self.cleaned_data.get('incident_date')
        if incident_date:
            from django.utils import timezone
            if incident_date > timezone.now():
                raise ValidationError("Incident date cannot be in the future.")
        return incident_date


class ComplianceFilterForm(forms.Form):
    """
    Form for filtering compliance data
    """
    COMPLIANCE_LEVELS = [
        ('', 'All Compliance Levels'),
        ('high', 'High (80-100%)'),
        ('medium', 'Medium (50-79%)'),
        ('low', 'Low (0-49%)'),
    ]
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by member name...'
        })
    )
    
    compliance_level = forms.ChoiceField(
        choices=COMPLIANCE_LEVELS,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    missing_insurance = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    missing_license = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    missing_training = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
