from django.contrib import admin
from .models import (MobileMoneyProvider, EWallet, WalletTransaction, 
                    MobileMoneyTransaction, DigitalToken, PaymentMethod, PaymentTransaction)


@admin.register(MobileMoneyProvider)
class MobileMoneyProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active', 'min_amount', 'max_amount', 'transaction_fee_percentage']
    list_filter = ['is_active']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'api_endpoint', 'is_active')
        }),
        ('Transaction Limits', {
            'fields': ('min_amount', 'max_amount')
        }),
        ('Fee Structure', {
            'fields': ('transaction_fee_percentage', 'fixed_transaction_fee')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(EWallet)
class EWalletAdmin(admin.ModelAdmin):
    list_display = ['wallet_id', 'member', 'balance', 'is_active', 'is_frozen', 'updated_at']
    list_filter = ['is_active', 'is_frozen', 'created_at']
    search_fields = ['wallet_id', 'member__user__first_name', 'member__user__last_name']
    readonly_fields = ['wallet_id', 'total_deposits', 'total_withdrawals', 'total_transfers', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Wallet Information', {
            'fields': ('member', 'wallet_id', 'balance')
        }),
        ('Security', {
            'fields': ('pin', 'is_active', 'is_frozen')
        }),
        ('Limits', {
            'fields': ('daily_limit', 'monthly_limit')
        }),
        ('Statistics', {
            'fields': ('total_deposits', 'total_withdrawals', 'total_transfers'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'wallet', 'transaction_type', 'amount', 'status', 'created_at']
    list_filter = ['transaction_type', 'status', 'created_at']
    search_fields = ['transaction_id', 'wallet__wallet_id', 'wallet__member__user__first_name', 'description']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'processed_at']
    
    fieldsets = (
        ('Transaction Details', {
            'fields': ('wallet', 'transaction_id', 'transaction_type', 'amount', 'fee')
        }),
        ('Status & References', {
            'fields': ('status', 'reference', 'description')
        }),
        ('Related Transactions', {
            'fields': ('related_wallet',)
        }),
        ('Balance Tracking', {
            'fields': ('balance_before', 'balance_after')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'processed_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MobileMoneyTransaction)
class MobileMoneyTransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'wallet', 'provider', 'transaction_type', 'amount', 'status', 'initiated_at']
    list_filter = ['provider', 'transaction_type', 'status', 'initiated_at']
    search_fields = ['transaction_id', 'provider_transaction_id', 'phone_number', 'wallet__wallet_id']
    date_hierarchy = 'initiated_at'
    readonly_fields = ['initiated_at', 'completed_at']
    
    fieldsets = (
        ('Transaction Details', {
            'fields': ('wallet', 'provider', 'transaction_id', 'provider_transaction_id', 'transaction_type')
        }),
        ('Amount & Fees', {
            'fields': ('amount', 'provider_fee', 'platform_fee')
        }),
        ('Mobile Money Details', {
            'fields': ('phone_number', 'account_name')
        }),
        ('Status & Processing', {
            'fields': ('status', 'error_message')
        }),
        ('Timestamps', {
            'fields': ('initiated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DigitalToken)
class DigitalTokenAdmin(admin.ModelAdmin):
    list_display = ['token_id', 'member', 'token_type', 'name', 'value', 'remaining_value', 'status', 'expiry_date']
    list_filter = ['token_type', 'status', 'expiry_date', 'issue_date']
    search_fields = ['token_id', 'name', 'member__user__first_name', 'member__user__last_name']
    date_hierarchy = 'expiry_date'
    readonly_fields = ['token_id', 'issue_date', 'created_at', 'used_at']
    
    fieldsets = (
        ('Token Information', {
            'fields': ('member', 'token_id', 'token_type', 'name', 'description')
        }),
        ('Value & Usage', {
            'fields': ('value', 'remaining_value', 'usage_count', 'max_usage')
        }),
        ('Validity', {
            'fields': ('issue_date', 'expiry_date')
        }),
        ('Status & Metadata', {
            'fields': ('status', 'issuer', 'merchant')
        }),
        ('QR Code', {
            'fields': ('qr_code',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'used_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['member', 'method_type', 'account_name', 'is_verified', 'is_default', 'is_active', 'last_used']
    list_filter = ['method_type', 'provider', 'is_verified', 'is_default', 'is_active']
    search_fields = ['member__user__first_name', 'member__user__last_name', 'account_name', 'account_number']
    readonly_fields = ['created_at', 'updated_at', 'last_used']
    
    fieldsets = (
        ('Method Details', {
            'fields': ('member', 'method_type', 'provider')
        }),
        ('Account Details', {
            'fields': ('account_number', 'account_name')
        }),
        ('Status', {
            'fields': ('is_verified', 'is_default', 'is_active')
        }),
        ('Metadata', {
            'fields': ('nickname', 'last_used')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'member', 'transaction_type', 'amount', 'status', 'initiated_at']
    list_filter = ['transaction_type', 'status', 'currency', 'initiated_at']
    search_fields = ['transaction_id', 'member__user__first_name', 'member__user__last_name', 'description', 'reference']
    date_hierarchy = 'initiated_at'
    readonly_fields = ['transaction_id', 'initiated_at', 'processed_at']
    
    fieldsets = (
        ('Transaction Details', {
            'fields': ('member', 'payment_method', 'transaction_id', 'transaction_type', 'amount', 'currency')
        }),
        ('Reference & Description', {
            'fields': ('reference', 'description')
        }),
        ('Related Objects', {
            'fields': ('contribution', 'loan')
        }),
        ('Status & Processing', {
            'fields': ('status', 'provider_response', 'error_message')
        }),
        ('Fees', {
            'fields': ('platform_fee', 'provider_fee')
        }),
        ('Timestamps', {
            'fields': ('initiated_at', 'processed_at'),
            'classes': ('collapse',)
        }),
    )
