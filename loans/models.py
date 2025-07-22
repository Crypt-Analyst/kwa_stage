from django.db import models
from decimal import Decimal

class Loan(models.Model):
    """
    Loan fund/kitty for small loans to members
    """
    LOAN_TYPES = [
        ('emergency', 'Emergency Loan'),
        ('bike_repair', 'Bike Repair'),
        ('fuel', 'Fuel Advance'),
        ('medical', 'Medical Emergency'),
        ('school_fees', 'School Fees'),
        ('business', 'Small Business'),
        ('other', 'Other'),
    ]
    
    LOAN_STATUS = [
        ('applied', 'Application Submitted'),
        ('approved', 'Approved'),
        ('disbursed', 'Disbursed'),
        ('repaying', 'Being Repaid'),
        ('completed', 'Fully Repaid'),
        ('defaulted', 'Defaulted'),
        ('written_off', 'Written Off'),
        ('rejected', 'Rejected'),
    ]
    
    loan_number = models.CharField(max_length=20, unique=True)
    member = models.ForeignKey('members.Member', on_delete=models.CASCADE, related_name='loans')
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
    status = models.CharField(max_length=20, choices=LOAN_STATUS, default='applied')
    
    # Loan amounts
    requested_amount = models.DecimalField(max_digits=10, decimal_places=2)
    approved_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    disbursed_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Interest and terms
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('5.00'), help_text="Monthly interest rate %")
    loan_term_months = models.PositiveIntegerField(default=6, help_text="Loan term in months")
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Important dates
    application_date = models.DateTimeField(auto_now_add=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    disbursement_date = models.DateTimeField(null=True, blank=True)
    expected_completion_date = models.DateField(null=True, blank=True)
    
    # Purpose and guarantors
    purpose = models.TextField()
    guarantor1 = models.ForeignKey(
        'members.Member', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='guaranteed_loans_1'
    )
    guarantor2 = models.ForeignKey(
        'members.Member', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='guaranteed_loans_2'
    )
    
    # Processing
    processed_by = models.ForeignKey(
        'members.Member', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='processed_loans'
    )
    approved_by = models.ForeignKey(
        'members.Member', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='approved_loans'
    )
    
    # Repayment tracking
    total_repaid = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    balance_remaining = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-application_date']
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'
    
    def __str__(self):
        return f"{self.loan_number} - {self.member.full_name} (KSh {self.requested_amount})"
    
    def calculate_monthly_payment(self):
        """Calculate monthly payment based on loan amount, interest rate, and term"""
        if self.approved_amount and self.interest_rate and self.loan_term_months:
            principal = float(self.approved_amount)
            monthly_rate = float(self.interest_rate) / 100
            num_payments = self.loan_term_months
            
            if monthly_rate > 0:
                payment = principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
            else:
                payment = principal / num_payments
            
            return Decimal(str(round(payment, 2)))
        return Decimal('0.00')
    
    def save(self, *args, **kwargs):
        if self.approved_amount and not self.monthly_payment:
            self.monthly_payment = self.calculate_monthly_payment()
        if self.approved_amount and not self.balance_remaining:
            self.balance_remaining = self.approved_amount
        super().save(*args, **kwargs)

class LoanRepayment(models.Model):
    """
    Track loan repayments
    """
    PAYMENT_METHODS = [
        ('mpesa', 'M-Pesa'),
        ('cash', 'Cash'),
        ('deduction', 'Salary/Earnings Deduction'),
        ('contribution_offset', 'Offset from Contributions'),
    ]
    
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='repayments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    
    # Payment details
    transaction_reference = models.CharField(max_length=100, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    
    # Split between principal and interest
    principal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Processing
    collected_by = models.ForeignKey(
        'members.Member', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='collected_repayments'
    )
    
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"{self.loan.loan_number} - KSh {self.amount} on {self.payment_date.date()}"

class LoanKitty(models.Model):
    """
    Track the overall loan fund/kitty balance
    """
    TRANSACTION_TYPES = [
        ('contribution', 'Kitty Contribution'),
        ('loan_disbursement', 'Loan Disbursement'),
        ('repayment', 'Loan Repayment'),
        ('interest_earned', 'Interest Earned'),
        ('penalty', 'Penalty Collection'),
        ('writeoff', 'Bad Debt Write-off'),
    ]
    
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_credit = models.BooleanField(help_text="True for money coming in, False for money going out")
    
    # References
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, null=True, blank=True)
    repayment = models.ForeignKey(LoanRepayment, on_delete=models.CASCADE, null=True, blank=True)
    
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
        """Calculate current loan kitty balance"""
        from django.db.models import Sum
        
        credits = cls.objects.filter(is_credit=True).aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0')
        
        debits = cls.objects.filter(is_credit=False).aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0')
        
        return credits - debits
