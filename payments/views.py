from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Sum
from django.utils import timezone
from django.core.paginator import Paginator
from decimal import Decimal
import uuid
from members.models import Member

from .models import (EWallet, WalletTransaction, MobileMoneyTransaction, 
                    DigitalToken, PaymentMethod, PaymentTransaction, MobileMoneyProvider)
from .forms import (EWalletTopupForm, TransferForm, PaymentMethodForm, 
                   TokenPurchaseForm, WithdrawalForm)


@login_required
def payments_dashboard(request):
    """
    Payments & Digital Services dashboard
    """
    try:
        member = request.user.member
        
        # Get or create e-wallet
        ewallet, created = EWallet.objects.get_or_create(
            member=member,
            defaults={'wallet_id': f'KW{member.id:06d}'}
        )
        
        # Recent transactions
        recent_transactions = WalletTransaction.objects.filter(wallet=ewallet)[:5]
        recent_payments = PaymentTransaction.objects.filter(member=member)[:5]
        
        # Active tokens
        active_tokens = DigitalToken.objects.filter(
            member=member,
            status='active',
            expiry_date__gt=timezone.now()
        )[:5]
        
        # Payment methods
        payment_methods = PaymentMethod.objects.filter(member=member, is_active=True)
        
        # Statistics
        total_deposits = WalletTransaction.objects.filter(
            wallet=ewallet,
            transaction_type='deposit',
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        total_payments = PaymentTransaction.objects.filter(
            member=member,
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        context = {
            'ewallet': ewallet,
            'recent_transactions': recent_transactions,
            'recent_payments': recent_payments,
            'active_tokens': active_tokens,
            'payment_methods': payment_methods,
            'total_deposits': total_deposits,
            'total_payments': total_payments,
        }
        
        return render(request, 'payments/dashboard.html', context)
    except Member.DoesNotExist:
        messages.error(request, "Please complete your member profile first.")
        return redirect('members:profile_setup')


@login_required
def wallet_transactions(request):
    """
    View all wallet transactions
    """
    member = request.user.member
    ewallet = get_object_or_404(EWallet, member=member)
    
    transactions = WalletTransaction.objects.filter(wallet=ewallet)
    
    # Filter by transaction type
    type_filter = request.GET.get('type')
    if type_filter:
        transactions = transactions.filter(transaction_type=type_filter)
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        transactions = transactions.filter(status=status_filter)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        transactions = transactions.filter(
            Q(transaction_id__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(reference__icontains=search_query)
        )
    
    paginator = Paginator(transactions, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'ewallet': ewallet,
        'page_obj': page_obj,
        'type_filter': type_filter,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    
    return render(request, 'payments/wallet_transactions.html', context)


@login_required
def topup_wallet(request):
    """
    Top up e-wallet using mobile money
    """
    member = request.user.member
    ewallet, created = EWallet.objects.get_or_create(
        member=member,
        defaults={'wallet_id': f'KW{member.id:06d}'}
    )
    
    if request.method == 'POST':
        form = EWalletTopupForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            provider = form.cleaned_data['provider']
            phone_number = form.cleaned_data['phone_number']
            
            # Create mobile money transaction
            transaction_id = f'TOP{uuid.uuid4().hex[:8].upper()}'
            
            mobile_transaction = MobileMoneyTransaction.objects.create(
                wallet=ewallet,
                provider=provider,
                transaction_id=transaction_id,
                transaction_type='deposit',
                amount=amount,
                phone_number=phone_number,
                status='initiated'
            )
            
            # In a real implementation, you would integrate with mobile money APIs here
            # For demo purposes, we'll simulate a successful transaction
            
            messages.success(request, f'Top-up request initiated. Transaction ID: {transaction_id}')
            return redirect('payments:wallet_transactions')
    else:
        form = EWalletTopupForm()
    
    context = {
        'form': form,
        'ewallet': ewallet,
    }
    
    return render(request, 'payments/topup_wallet.html', context)


@login_required
def transfer_funds(request):
    """
    Transfer funds to another member's wallet
    """
    member = request.user.member
    ewallet = get_object_or_404(EWallet, member=member)
    
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            recipient_phone = form.cleaned_data['recipient_phone']
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            
            try:
                # Find recipient member by phone
                from members.models import Member
                recipient_member = Member.objects.get(phone_number=recipient_phone)
                recipient_wallet, created = EWallet.objects.get_or_create(
                    member=recipient_member,
                    defaults={'wallet_id': f'KW{recipient_member.id:06d}'}
                )
                
                # Check if sender has sufficient funds
                if ewallet.balance >= amount:
                    # Deduct from sender
                    ewallet.deduct_funds(amount, f"Transfer to {recipient_member.user.get_full_name()}")
                    
                    # Add to recipient
                    recipient_wallet.add_funds(amount, f"Transfer from {member.user.get_full_name()}")
                    
                    messages.success(request, f'Successfully transferred KES {amount} to {recipient_member.user.get_full_name()}')
                    return redirect('payments:wallet_transactions')
                else:
                    messages.error(request, 'Insufficient funds in your wallet.')
            
            except Member.DoesNotExist:
                messages.error(request, 'Recipient not found. Please check the phone number.')
    else:
        form = TransferForm()
    
    context = {
        'form': form,
        'ewallet': ewallet,
    }
    
    return render(request, 'payments/transfer_funds.html', context)


@login_required
def withdraw_funds(request):
    """
    Withdraw funds from e-wallet to mobile money
    """
    member = request.user.member
    ewallet = get_object_or_404(EWallet, member=member)
    
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            provider = form.cleaned_data['provider']
            phone_number = form.cleaned_data['phone_number']
            
            # Check if user has sufficient funds
            if ewallet.balance >= amount:
                # Create mobile money transaction
                transaction_id = f'WTH{uuid.uuid4().hex[:8].upper()}'
                
                mobile_transaction = MobileMoneyTransaction.objects.create(
                    wallet=ewallet,
                    provider=provider,
                    transaction_id=transaction_id,
                    transaction_type='withdrawal',
                    amount=amount,
                    phone_number=phone_number,
                    status='initiated'
                )
                
                # Deduct funds from wallet (pending confirmation)
                ewallet.deduct_funds(amount, f"Withdrawal to {provider.name}")
                
                messages.success(request, f'Withdrawal request initiated. Transaction ID: {transaction_id}')
                return redirect('payments:wallet_transactions')
            else:
                messages.error(request, 'Insufficient funds in your wallet.')
    else:
        form = WithdrawalForm()
    
    context = {
        'form': form,
        'ewallet': ewallet,
    }
    
    return render(request, 'payments/withdraw_funds.html', context)


@login_required
def digital_tokens(request):
    """
    View all digital tokens
    """
    member = request.user.member
    tokens = DigitalToken.objects.filter(member=member)
    
    # Filter by token type
    type_filter = request.GET.get('type')
    if type_filter:
        tokens = tokens.filter(token_type=type_filter)
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        tokens = tokens.filter(status=status_filter)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        tokens = tokens.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(token_id__icontains=search_query)
        )
    
    paginator = Paginator(tokens, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'type_filter': type_filter,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    
    return render(request, 'payments/digital_tokens.html', context)


@login_required
def purchase_token(request):
    """
    Purchase digital tokens
    """
    member = request.user.member
    ewallet = get_object_or_404(EWallet, member=member)
    
    if request.method == 'POST':
        form = TokenPurchaseForm(request.POST)
        if form.is_valid():
            token_type = form.cleaned_data['token_type']
            quantity = form.cleaned_data['quantity']
            
            # Token pricing (in a real app, this would be configurable)
            token_prices = {
                'stage_pass': Decimal('50.00'),
                'parking_token': Decimal('20.00'),
                'fuel_voucher': Decimal('100.00'),
                'service_credit': Decimal('25.00'),
            }
            
            if token_type in token_prices:
                total_cost = token_prices[token_type] * quantity
                
                if ewallet.balance >= total_cost:
                    # Deduct funds
                    ewallet.deduct_funds(total_cost, f"Purchase {quantity}x {token_type}")
                    
                    # Create tokens
                    for i in range(quantity):
                        DigitalToken.objects.create(
                            member=member,
                            token_id=f'{token_type.upper()}{uuid.uuid4().hex[:8].upper()}',
                            token_type=token_type,
                            name=f"{token_type.replace('_', ' ').title()}",
                            description=f"Digital {token_type.replace('_', ' ')} token",
                            value=token_prices[token_type],
                            remaining_value=token_prices[token_type],
                            expiry_date=timezone.now() + timezone.timedelta(days=90)
                        )
                    
                    messages.success(request, f'Successfully purchased {quantity} {token_type} token(s) for KES {total_cost}')
                    return redirect('payments:digital_tokens')
                else:
                    messages.error(request, 'Insufficient funds in your wallet.')
            else:
                messages.error(request, 'Invalid token type.')
    else:
        form = TokenPurchaseForm()
    
    context = {
        'form': form,
        'ewallet': ewallet,
    }
    
    return render(request, 'payments/purchase_token.html', context)


@login_required
def payment_methods(request):
    """
    Manage payment methods
    """
    member = request.user.member
    methods = PaymentMethod.objects.filter(member=member, is_active=True)
    
    context = {
        'payment_methods': methods,
    }
    
    return render(request, 'payments/payment_methods.html', context)


@login_required
def add_payment_method(request):
    """
    Add new payment method
    """
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            payment_method = form.save(commit=False)
            payment_method.member = request.user.member
            payment_method.save()
            messages.success(request, 'Payment method added successfully!')
            return redirect('payments:payment_methods')
    else:
        form = PaymentMethodForm()
    
    return render(request, 'payments/add_payment_method.html', {'form': form})


@login_required
def payment_history(request):
    """
    View payment transaction history
    """
    member = request.user.member
    payments = PaymentTransaction.objects.filter(member=member)
    
    # Filter by transaction type
    type_filter = request.GET.get('type')
    if type_filter:
        payments = payments.filter(transaction_type=type_filter)
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        payments = payments.filter(status=status_filter)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        payments = payments.filter(
            Q(transaction_id__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(reference__icontains=search_query)
        )
    
    paginator = Paginator(payments, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'type_filter': type_filter,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    
    return render(request, 'payments/payment_history.html', context)


@login_required
def transaction_details(request, transaction_id):
    """
    View detailed transaction information
    """
    member = request.user.member
    
    # Try to find transaction in different models
    transaction = None
    transaction_type = None
    
    try:
        ewallet = EWallet.objects.get(member=member)
        transaction = WalletTransaction.objects.get(
            wallet=ewallet,
            transaction_id=transaction_id
        )
        transaction_type = 'wallet'
    except (WalletTransaction.DoesNotExist, EWallet.DoesNotExist):
        try:
            transaction = PaymentTransaction.objects.get(
                member=member,
                transaction_id=transaction_id
            )
            transaction_type = 'payment'
        except PaymentTransaction.DoesNotExist:
            try:
                ewallet = EWallet.objects.get(member=member)
                transaction = MobileMoneyTransaction.objects.get(
                    wallet=ewallet,
                    transaction_id=transaction_id
                )
                transaction_type = 'mobile_money'
            except (MobileMoneyTransaction.DoesNotExist, EWallet.DoesNotExist):
                messages.error(request, 'Transaction not found.')
                return redirect('payments:dashboard')
    
    context = {
        'transaction': transaction,
        'transaction_type': transaction_type,
    }
    
    return render(request, 'payments/transaction_details.html', context)
