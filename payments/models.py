from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from members.models import Member

class MobileMoneyProvider(models.Model):
    """
    Mobile money service providers
    """
    name = models.CharField(max_length=100, unique=True)  # M-Pesa, Airtel Money, etc.
    code = models.CharField(max_length=10, unique=True)   # MPESA, AIRTEL, etc.
    api_endpoint = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    
    # Transaction limits
    min_amount = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    max_amount = models.DecimalField(max_digits=10, decimal_places=2, default=70000.00)
    
    # Fees structure
    transaction_fee_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    fixed_transaction_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class EWallet(models.Model):
    """
    Digital wallet for each member
    """
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='ewallet')
    
    # Wallet details
    wallet_id = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Security
    pin = models.CharField(max_length=128, help_text="Hashed PIN for wallet access")
    is_active = models.BooleanField(default=True)
    is_frozen = models.BooleanField(default=False)
    
    # Limits
    daily_limit = models.DecimalField(max_digits=10, decimal_places=2, default=10000.00)
    monthly_limit = models.DecimalField(max_digits=12, decimal_places=2, default=100000.00)
    
    # Tracking
    total_deposits = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_withdrawals = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_transfers = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Wallet - {self.member.user.get_full_name()} (KES {self.balance})"
    
    def add_funds(self, amount, description=""):
        """Add funds to wallet"""
        self.balance += Decimal(str(amount))
        self.total_deposits += Decimal(str(amount))
        self.save()
        
        # Create transaction record
        WalletTransaction.objects.create(
            wallet=self,
            transaction_type='deposit',
            amount=amount,
            description=description,
            balance_after=self.balance
        )
    
    def deduct_funds(self, amount, description=""):
        """Deduct funds from wallet"""
        if self.balance >= Decimal(str(amount)):
            self.balance -= Decimal(str(amount))
            self.total_withdrawals += Decimal(str(amount))
            self.save()
            
            # Create transaction record
            WalletTransaction.objects.create(
                wallet=self,
                transaction_type='withdrawal',
                amount=amount,
                description=description,
                balance_after=self.balance
            )
            return True
        return False

class WalletTransaction(models.Model):
    """
    All wallet transactions
    """
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer_in', 'Transfer In'),
        ('transfer_out', 'Transfer Out'),
        ('payment', 'Payment'),
        ('refund', 'Refund'),
        ('fee', 'Fee'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    wallet = models.ForeignKey(EWallet, on_delete=models.CASCADE, related_name='transactions')
    
    # Transaction details
    transaction_id = models.CharField(max_length=50, unique=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    
    # Status and references
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reference = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    
    # Related transactions (for transfers)
    related_wallet = models.ForeignKey(EWallet, on_delete=models.SET_NULL, blank=True, null=True,
                                      related_name='related_transactions')
    
    # Balance tracking
    balance_before = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after = models.DecimalField(max_digits=12, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.transaction_id} - {self.get_transaction_type_display()} (KES {self.amount})"

class MobileMoneyTransaction(models.Model):
    """
    Mobile money transactions (deposits/withdrawals)
    """
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit to Wallet'),
        ('withdrawal', 'Withdrawal from Wallet'),
    ]
    
    STATUS_CHOICES = [
        ('initiated', 'Initiated'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    wallet = models.ForeignKey(EWallet, on_delete=models.CASCADE, related_name='mobile_transactions')
    provider = models.ForeignKey(MobileMoneyProvider, on_delete=models.CASCADE)
    
    # Transaction details
    transaction_id = models.CharField(max_length=50, unique=True)
    provider_transaction_id = models.CharField(max_length=100, blank=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    
    # Amount and fees
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    provider_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    platform_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    
    # Mobile money details
    phone_number = models.CharField(max_length=20)
    account_name = models.CharField(max_length=200, blank=True)
    
    # Status and processing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='initiated')
    error_message = models.TextField(blank=True)
    
    # Timestamps
    initiated_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-initiated_at']
    
    def __str__(self):
        return f"{self.provider.name} {self.get_transaction_type_display()} - KES {self.amount}"

class DigitalToken(models.Model):
    """
    Digital tokens for various services
    """
    TOKEN_TYPES = [
        ('stage_pass', 'Stage Pass'),
        ('parking_token', 'Parking Token'),
        ('fuel_voucher', 'Fuel Voucher'),
        ('service_credit', 'Service Credit'),
        ('loyalty_point', 'Loyalty Point'),
        ('discount_coupon', 'Discount Coupon'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('used', 'Used'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='digital_tokens')
    
    # Token details
    token_id = models.CharField(max_length=50, unique=True)
    token_type = models.CharField(max_length=20, choices=TOKEN_TYPES)
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # Value and usage
    value = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_value = models.DecimalField(max_digits=10, decimal_places=2)
    usage_count = models.PositiveIntegerField(default=0)
    max_usage = models.PositiveIntegerField(default=1)
    
    # Validity
    issue_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    
    # Status and metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    issuer = models.CharField(max_length=200, blank=True)
    merchant = models.CharField(max_length=200, blank=True)
    
    # QR code for redemption
    qr_code = models.ImageField(upload_to='token_qr_codes/', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.member.user.get_full_name()}"
    
    @property
    def is_valid(self):
        from django.utils import timezone
        return (self.status == 'active' and 
                self.expiry_date > timezone.now() and 
                self.usage_count < self.max_usage)
    
    def redeem(self, amount=None):
        """Redeem token (full or partial)"""
        if not self.is_valid:
            return False
        
        if amount is None:
            amount = self.remaining_value
        
        if amount <= self.remaining_value:
            self.remaining_value -= Decimal(str(amount))
            self.usage_count += 1
            
            if self.remaining_value <= 0 or self.usage_count >= self.max_usage:
                self.status = 'used'
                self.used_at = timezone.now()
            
            self.save()
            return True
        return False

class PaymentMethod(models.Model):
    """
    Saved payment methods for members
    """
    METHOD_TYPES = [
        ('mobile_money', 'Mobile Money'),
        ('bank_card', 'Bank Card'),
        ('bank_account', 'Bank Account'),
        ('ewallet', 'E-Wallet'),
    ]
    
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='payment_methods')
    
    # Method details
    method_type = models.CharField(max_length=20, choices=METHOD_TYPES)
    provider = models.ForeignKey(MobileMoneyProvider, on_delete=models.CASCADE, blank=True, null=True)
    
    # Account details (encrypted/masked)
    account_number = models.CharField(max_length=100)  # Phone number, card number, etc.
    account_name = models.CharField(max_length=200)
    
    # Status
    is_verified = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Metadata
    nickname = models.CharField(max_length=100, blank=True)
    last_used = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_default', '-last_used']
    
    def __str__(self):
        return f"{self.get_method_type_display()} - {self.account_name}"

class PaymentTransaction(models.Model):
    """
    All payment transactions in the system
    """
    TRANSACTION_TYPES = [
        ('contribution', 'Contribution Payment'),
        ('loan_payment', 'Loan Payment'),
        ('emergency_fund', 'Emergency Fund'),
        ('service_fee', 'Service Fee'),
        ('token_purchase', 'Token Purchase'),
        ('wallet_topup', 'Wallet Top-up'),
        ('transfer', 'Transfer'),
        ('withdrawal', 'Withdrawal'),
    ]
    
    STATUS_CHOICES = [
        ('initiated', 'Initiated'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='payment_transactions')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, blank=True, null=True)
    
    # Transaction details
    transaction_id = models.CharField(max_length=50, unique=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    
    # Reference and description
    reference = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    
    # Related objects
    contribution = models.ForeignKey('contributions.Contribution', on_delete=models.SET_NULL, 
                                   blank=True, null=True)
    loan = models.ForeignKey('loans.Loan', on_delete=models.SET_NULL, blank=True, null=True)
    
    # Status and processing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='initiated')
    provider_response = models.JSONField(blank=True, null=True)
    error_message = models.TextField(blank=True)
    
    # Fees
    platform_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    provider_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    
    # Timestamps
    initiated_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-initiated_at']
    
    def __str__(self):
        return f"{self.transaction_id} - {self.get_transaction_type_display()} (KES {self.amount})"
