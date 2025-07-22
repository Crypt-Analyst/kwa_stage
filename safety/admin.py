from django.contrib import admin
from .models import Insurance, License, SafetyTraining, ComplianceChecklist, SafetyIncident


@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = ['policy_number', 'member', 'insurance_type', 'insurance_company', 'status', 'end_date']
    list_filter = ['insurance_type', 'status', 'insurance_company', 'end_date']
    search_fields = ['policy_number', 'member__user__first_name', 'member__user__last_name', 'insurance_company']
    date_hierarchy = 'end_date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('member', 'insurance_type', 'policy_number', 'insurance_company')
        }),
        ('Financial Details', {
            'fields': ('coverage_amount', 'premium_amount')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date', 'reminder_date')
        }),
        ('Status & Documents', {
            'fields': ('status', 'policy_document')
        }),
        ('Contact Information', {
            'fields': ('agent_name', 'agent_phone')
        }),
        ('Statistics', {
            'fields': ('claims_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ['license_number', 'member', 'license_type', 'issuing_authority', 'status', 'expiry_date']
    list_filter = ['license_type', 'status', 'issuing_authority', 'expiry_date']
    search_fields = ['license_number', 'member__user__first_name', 'member__user__last_name', 'issuing_authority']
    date_hierarchy = 'expiry_date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('member', 'license_type', 'license_number', 'issuing_authority')
        }),
        ('Dates', {
            'fields': ('issue_date', 'expiry_date', 'reminder_date')
        }),
        ('Status & Documents', {
            'fields': ('status', 'license_document')
        }),
        ('Additional Information', {
            'fields': ('restrictions', 'endorsements')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SafetyTraining)
class SafetyTrainingAdmin(admin.ModelAdmin):
    list_display = ['training_title', 'member', 'training_type', 'status', 'scheduled_date', 'passed']
    list_filter = ['training_type', 'status', 'passed', 'scheduled_date', 'training_institution']
    search_fields = ['training_title', 'member__user__first_name', 'member__user__last_name', 'trainer_name']
    date_hierarchy = 'scheduled_date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('member', 'training_type', 'training_title', 'description')
        }),
        ('Training Details', {
            'fields': ('trainer_name', 'training_institution', 'venue')
        }),
        ('Schedule & Duration', {
            'fields': ('scheduled_date', 'completed_date', 'duration_hours')
        }),
        ('Assessment', {
            'fields': ('status', 'score', 'passed')
        }),
        ('Documents', {
            'fields': ('certificate', 'attendance_sheet')
        }),
        ('Renewal Information', {
            'fields': ('certificate_expiry', 'renewal_required')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SafetyIncident)
class SafetyIncidentAdmin(admin.ModelAdmin):
    list_display = ['title', 'reporter', 'incident_type', 'severity', 'incident_date', 'is_resolved']
    list_filter = ['incident_type', 'severity', 'is_resolved', 'investigation_required', 'incident_date']
    search_fields = ['title', 'description', 'location', 'reporter__user__first_name', 'reporter__user__last_name']
    date_hierarchy = 'incident_date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('reporter', 'involved_member', 'incident_type', 'severity')
        }),
        ('Incident Details', {
            'fields': ('title', 'description', 'location', 'incident_date')
        }),
        ('Actions & Follow-up', {
            'fields': ('action_taken', 'preventive_measures', 'investigation_required', 'investigation_completed')
        }),
        ('Resolution', {
            'fields': ('is_resolved', 'resolution_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ComplianceChecklist)
class ComplianceChecklistAdmin(admin.ModelAdmin):
    list_display = ['member', 'compliance_score', 'stage_membership_active', 'last_updated']
    list_filter = ['bike_insurance_valid', 'driving_license_valid', 'safety_training_completed', 'stage_membership_active']
    search_fields = ['member__user__first_name', 'member__user__last_name']
    readonly_fields = ['compliance_score', 'last_updated']
    
    fieldsets = (
        ('Member', {
            'fields': ('member',)
        }),
        ('Insurance Compliance', {
            'fields': ('bike_insurance_valid', 'personal_insurance_valid')
        }),
        ('License Compliance', {
            'fields': ('driving_license_valid', 'motorcycle_permit_valid', 'commercial_permit_valid')
        }),
        ('Training Compliance', {
            'fields': ('safety_training_completed', 'first_aid_training_completed')
        }),
        ('Additional Requirements', {
            'fields': ('good_conduct_certificate', 'stage_membership_active')
        }),
        ('Score & Updates', {
            'fields': ('compliance_score', 'last_updated'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['recalculate_compliance_scores']
    
    def recalculate_compliance_scores(self, request, queryset):
        """Admin action to recalculate compliance scores"""
        for compliance in queryset:
            compliance.calculate_compliance_score()
        self.message_user(request, f"Recalculated compliance scores for {queryset.count()} members.")
    recalculate_compliance_scores.short_description = "Recalculate compliance scores"
