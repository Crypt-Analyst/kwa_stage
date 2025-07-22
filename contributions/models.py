from django.db import models
from decimal import Decimal

class Contribution(models.Model):
    """
    Track member contributions (weekly/monthly payments)
    """
    CONTRIBUTION_TYPES = [
        ('weekly', 'Weekly Contribution'),
        ('monthly', 'Monthly Contribution'),
        ('emergency', 'Emergency Contribution'),
        ('loan_repayment', 'Loan Repayment'),
        ('penalty', 'Penalty Payment'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHODS = [
        ('mpesa', 'M-Pesa'),
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_money', 'Mobile Money'),
    ]
    
    member = models.ForeignKey('members.Member', on_delete=models.CASCADE, related_name='contributions')
    contribution_type = models.CharField(max_length=20, choices=CONTRIBUTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    
    # Payment details
    transaction_id = models.CharField(max_length=100, unique=True, blank=True)
    mpesa_code = models.CharField(max_length=20, blank=True, help_text="M-Pesa confirmation code")
    payment_phone = models.CharField(max_length=15, blank=True)
    
    # Status and dates
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    
    # Additional information
    description = models.TextField(blank=True)
    collected_by = models.ForeignKey(
        'members.Member', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='collected_contributions',
        help_text="Stage leader or official who collected the contribution"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-payment_date']
        verbose_name = 'Contribution'
        verbose_name_plural = 'Contributions'
    
    def __str__(self):
        return f"{self.member.full_name} - KSh {self.amount} ({self.get_contribution_type_display()})"

class ContributionPlan(models.Model):
    """
    Define contribution plans and schedules
    """
    PLAN_TYPES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
    ]
    
    name = models.CharField(max_length=200)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    
    # Auto-assignment rules
    stage = models.ForeignKey('stages.Stage', on_delete=models.CASCADE, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - KSh {self.amount} ({self.get_plan_type_display()})"

class WelfareAccount(models.Model):
    """
    Track the main welfare account balance and transactions
    """
    TRANSACTION_TYPES = [
        ('contribution', 'Member Contribution'),
        ('disbursement', 'Emergency Disbursement'),
        ('loan', 'Loan Disbursement'),
        ('loan_repayment', 'Loan Repayment'),
        ('penalty', 'Penalty Collection'),
        ('expense', 'Administrative Expense'),
        ('interest', 'Interest Earned'),
    ]
    
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_credit = models.BooleanField(help_text="True for money coming in, False for money going out")
    
    # References
    contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE, null=True, blank=True)
    emergency_case = models.ForeignKey('emergency.EmergencyCase', on_delete=models.CASCADE, null=True, blank=True)
    loan = models.ForeignKey('loans.Loan', on_delete=models.CASCADE, null=True, blank=True)
    
    description = models.TextField()
    processed_by = models.ForeignKey('members.Member', on_delete=models.SET_NULL, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        direction = "Credit" if self.is_credit else "Debit"
        return f"{direction}: KSh {self.amount} - {self.get_transaction_type_display()}"
    
    @classmethod
    def get_current_balance(cls):
        """Calculate current welfare account balance"""
        from django.db.models import Sum, Q
        
        credits = cls.objects.filter(is_credit=True).aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0')
        
        debits = cls.objects.filter(is_credit=False).aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0')
        
        return credits - debits
