from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Dashboard
    path('', views.payments_dashboard, name='dashboard'),
    
    # E-Wallet
    path('wallet/transactions/', views.wallet_transactions, name='wallet_transactions'),
    path('wallet/topup/', views.topup_wallet, name='topup'),
    path('wallet/transfer/', views.transfer_funds, name='transfer'),
    path('wallet/withdraw/', views.withdraw_funds, name='withdraw'),
    
    # Digital Tokens
    path('tokens/', views.digital_tokens, name='digital_tokens'),
    path('tokens/purchase/', views.purchase_token, name='purchase_token'),
    
    # Payment Methods
    path('methods/', views.payment_methods, name='payment_methods'),
    path('methods/add/', views.add_payment_method, name='add_payment_method'),
    
    # Payment History
    path('history/', views.payment_history, name='payment_history'),
    path('transaction/<str:transaction_id>/', views.transaction_details, name='transaction_details'),
]
