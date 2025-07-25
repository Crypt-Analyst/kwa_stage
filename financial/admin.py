from django.contrib import admin
from .models import (
    SaccoProvider, BankProvider, SaccoApplication, 
    BankLoanApplication, ApplicationDocument, LoanCalculation
)

@admin.register(SaccoProvider)
class SaccoProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'coverage_area', 'bodaboda_focused', 'is_active', 'rating']
    list_filter = ['bodaboda_focused', 'is_active', 'coverage_area', 'offers_motorcycle_loans']
    search_fields = ['name', 'sacco_code', 'counties_served']
    readonly_fields = ['created_at', 'updated_at', 'total_applications_processed']

@admin.register(BankProvider)
class BankProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'bank_code', 'nationwide_coverage', 'is_active', 'rating']
    list_filter = ['nationwide_coverage', 'is_active', 'offers_motorcycle_loans']
    search_fields = ['name', 'bank_code']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(SaccoApplication)
class SaccoApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'sacco', 'application_type', 'status', 'requested_amount', 'created_at']
    list_filter = ['application_type', 'status', 'created_at']
    search_fields = ['applicant__user__first_name', 'applicant__user__last_name', 'sacco__name']
    readonly_fields = ['application_id', 'created_at', 'updated_at']

@admin.register(BankLoanApplication)
class BankLoanApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'bank', 'loan_type', 'status', 'requested_amount', 'created_at']
    list_filter = ['loan_type', 'status', 'created_at']
    search_fields = ['applicant__user__first_name', 'applicant__user__last_name', 'bank__name']
    readonly_fields = ['application_id', 'created_at', 'updated_at']

@admin.register(ApplicationDocument)
class ApplicationDocumentAdmin(admin.ModelAdmin):
    list_display = ['document_name', 'document_type', 'is_verified', 'uploaded_at']
    list_filter = ['document_type', 'is_verified', 'uploaded_at']
    readonly_fields = ['file_size', 'uploaded_at', 'updated_at']

@admin.register(LoanCalculation)
class LoanCalculationAdmin(admin.ModelAdmin):
    list_display = ['member', 'provider_type', 'provider_name', 'principal_amount', 'monthly_payment', 'created_at']
    list_filter = ['provider_type', 'created_at']
    readonly_fields = ['created_at']
