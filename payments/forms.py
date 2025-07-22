from django import forms
from django.core.exceptions import ValidationError
from decimal import Decimal

from .models import EWallet, PaymentMethod, MobileMoneyProvider, DigitalToken


class EWalletTopupForm(forms.Form):
    """
    Form for topping up e-wallet using mobile money
    """
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('1.00'),
        max_value=Decimal('70000.00'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Enter amount (KES)',
        }),
        label='Amount (KES)'
    )
    
    provider = forms.ModelChoiceField(
        queryset=MobileMoneyProvider.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Mobile Money Provider'
    )
    
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 0722123456',
            'pattern': '^(07|01)\d{8}$'
        }),
        label='Phone Number',
        help_text='Enter your mobile money phone number'
    )
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            # Basic Kenyan phone number validation
            if not phone.startswith(('07', '01')) or len(phone) != 10:
                raise ValidationError("Please enter a valid Kenyan phone number (e.g., 0722123456)")
        return phone


class TransferForm(forms.Form):
    """
    Form for transferring funds between wallets
    """
    recipient_phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 0722123456',
            'pattern': '^(07|01)\d{8}$'
        }),
        label='Recipient Phone Number',
        help_text='Phone number of the member to transfer to'
    )
    
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('1.00'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Enter amount (KES)',
        }),
        label='Amount (KES)'
    )
    
    description = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Optional description for the transfer',
        }),
        label='Description (Optional)'
    )
    
    def clean_recipient_phone(self):
        phone = self.cleaned_data.get('recipient_phone')
        if phone:
            # Basic Kenyan phone number validation
            if not phone.startswith(('07', '01')) or len(phone) != 10:
                raise ValidationError("Please enter a valid Kenyan phone number (e.g., 0722123456)")
        return phone


class WithdrawalForm(forms.Form):
    """
    Form for withdrawing funds from e-wallet to mobile money
    """
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('1.00'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Enter amount (KES)',
        }),
        label='Amount (KES)'
    )
    
    provider = forms.ModelChoiceField(
        queryset=MobileMoneyProvider.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Mobile Money Provider'
    )
    
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 0722123456',
            'pattern': '^(07|01)\d{8}$'
        }),
        label='Phone Number',
        help_text='Enter your mobile money phone number'
    )
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            # Basic Kenyan phone number validation
            if not phone.startswith(('07', '01')) or len(phone) != 10:
                raise ValidationError("Please enter a valid Kenyan phone number (e.g., 0722123456)")
        return phone


class PaymentMethodForm(forms.ModelForm):
    """
    Form for adding payment methods
    """
    
    class Meta:
        model = PaymentMethod
        fields = ['method_type', 'provider', 'account_number', 'account_name', 'nickname']
        widgets = {
            'method_type': forms.Select(attrs={'class': 'form-control'}),
            'provider': forms.Select(attrs={'class': 'form-control'}),
            'account_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number, card number, or account number'
            }),
            'account_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Account holder name'
            }),
            'nickname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional nickname for this payment method'
            }),
        }
        labels = {
            'method_type': 'Payment Method Type',
            'provider': 'Provider',
            'account_number': 'Account Number/Phone',
            'account_name': 'Account Name',
            'nickname': 'Nickname (Optional)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['provider'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        method_type = cleaned_data.get('method_type')
        provider = cleaned_data.get('provider')
        account_number = cleaned_data.get('account_number')
        
        if method_type == 'mobile_money' and not provider:
            raise ValidationError("Provider is required for mobile money payments.")
        
        if method_type == 'mobile_money' and account_number:
            # Validate phone number for mobile money
            if not account_number.startswith(('07', '01')) or len(account_number) != 10:
                raise ValidationError("Please enter a valid Kenyan phone number for mobile money.")
        
        return cleaned_data


class TokenPurchaseForm(forms.Form):
    """
    Form for purchasing digital tokens
    """
    TOKEN_CHOICES = [
        ('stage_pass', 'Stage Pass (KES 50)'),
        ('parking_token', 'Parking Token (KES 20)'),
        ('fuel_voucher', 'Fuel Voucher (KES 100)'),
        ('service_credit', 'Service Credit (KES 25)'),
    ]
    
    token_type = forms.ChoiceField(
        choices=TOKEN_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Token Type'
    )
    
    quantity = forms.IntegerField(
        min_value=1,
        max_value=50,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'max': '50',
            'value': '1'
        }),
        label='Quantity',
        help_text='Maximum 50 tokens per purchase'
    )


class PaymentFilterForm(forms.Form):
    """
    Form for filtering payment transactions
    """
    TRANSACTION_TYPE_CHOICES = [
        ('', 'All Transaction Types'),
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
        ('', 'All Statuses'),
        ('initiated', 'Initiated'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by transaction ID, reference, or description...'
        }),
        label='Search'
    )
    
    transaction_type = forms.ChoiceField(
        choices=TRANSACTION_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Transaction Type'
    )
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Status'
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='From Date'
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='To Date'
    )


class WalletTransactionFilterForm(forms.Form):
    """
    Form for filtering wallet transactions
    """
    TRANSACTION_TYPE_CHOICES = [
        ('', 'All Transaction Types'),
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer_in', 'Transfer In'),
        ('transfer_out', 'Transfer Out'),
        ('payment', 'Payment'),
        ('refund', 'Refund'),
        ('fee', 'Fee'),
    ]
    
    STATUS_CHOICES = [
        ('', 'All Statuses'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by transaction ID, reference, or description...'
        }),
        label='Search'
    )
    
    transaction_type = forms.ChoiceField(
        choices=TRANSACTION_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Transaction Type'
    )
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Status'
    )


class TokenFilterForm(forms.Form):
    """
    Form for filtering digital tokens
    """
    TOKEN_TYPE_CHOICES = [
        ('', 'All Token Types'),
        ('stage_pass', 'Stage Pass'),
        ('parking_token', 'Parking Token'),
        ('fuel_voucher', 'Fuel Voucher'),
        ('service_credit', 'Service Credit'),
        ('loyalty_point', 'Loyalty Point'),
        ('discount_coupon', 'Discount Coupon'),
    ]
    
    STATUS_CHOICES = [
        ('', 'All Statuses'),
        ('active', 'Active'),
        ('used', 'Used'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by token name, ID, or description...'
        }),
        label='Search'
    )
    
    token_type = forms.ChoiceField(
        choices=TOKEN_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Token Type'
    )
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Status'
    )
