#!/usr/bin/env python3
"""
Create sample SACCO data for testing
"""
import os
import sys
import django

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bodaboda_welfare.settings')
django.setup()

from financial.models import SaccoProvider, BankProvider

def create_sample_saccos():
    """Create sample SACCO providers"""
    saccos_data = [
        {
            'name': 'Boda Boda SACCO',
            'sacco_code': 'BB001',
            'phone_number': '+254700123456',
            'email': 'info@bodabodasacco.co.ke',
            'website': 'https://bodabodasacco.co.ke',
            'physical_address': 'Tom Mboya Street, Nairobi',
            'coverage_area': 'Nationwide',
            'counties_served': 'Nairobi, Kiambu, Machakos, Kajiado, Murang\'a',
            'headquarters_location': 'Nairobi',
            'registration_number': 'CS/001/2020',
            'is_active': True,
            'bodaboda_focused': True,
            'min_loan_amount': 10000,
            'max_loan_amount': 500000,
            'interest_rate_min': 12.0,
            'interest_rate_max': 18.0,
        },
        {
            'name': 'Transport Operators SACCO',
            'sacco_code': 'TO002',
            'phone_number': '+254720234567',
            'email': 'contact@transportoperators.co.ke',
            'physical_address': 'Ronald Ngala Street, Nairobi',
            'coverage_area': 'Central Region',
            'counties_served': 'Nairobi, Kiambu, Nyeri, Murang\'a, Kirinyaga',
            'headquarters_location': 'Nairobi',
            'registration_number': 'CS/002/2019',
            'is_active': True,
            'bodaboda_focused': True,
            'min_loan_amount': 15000,
            'max_loan_amount': 750000,
            'interest_rate_min': 14.0,
            'interest_rate_max': 20.0,
        },
        {
            'name': 'Motorcycle Riders SACCO',
            'sacco_code': 'MR003',
            'phone_number': '+254733345678',
            'email': 'info@motorcycleriders.co.ke',
            'physical_address': 'Moi Avenue, Mombasa',
            'coverage_area': 'Coast Region',
            'counties_served': 'Mombasa, Kilifi, Kwale, Taita Taveta',
            'headquarters_location': 'Mombasa',
            'registration_number': 'CS/003/2021',
            'is_active': True,
            'bodaboda_focused': True,
            'min_loan_amount': 8000,
            'max_loan_amount': 400000,
            'interest_rate_min': 15.0,
            'interest_rate_max': 22.0,
        },
        {
            'name': 'Western Transport SACCO',
            'sacco_code': 'WT004',
            'phone_number': '+254744456789',
            'email': 'contact@westerntransport.co.ke',
            'physical_address': 'Kakamega Road, Kakamega',
            'coverage_area': 'Western Region',
            'counties_served': 'Kakamega, Bungoma, Vihiga, Busia',
            'headquarters_location': 'Kakamega',
            'registration_number': 'CS/004/2020',
            'is_active': True,
            'bodaboda_focused': True,
            'min_loan_amount': 12000,
            'max_loan_amount': 600000,
            'interest_rate_min': 13.0,
            'interest_rate_max': 19.0,
        },
        {
            'name': 'Rift Valley Riders SACCO',
            'sacco_code': 'RV005',
            'phone_number': '+254755567890',
            'email': 'info@riftvalleyriders.co.ke',
            'physical_address': 'Kenyatta Avenue, Nakuru',
            'coverage_area': 'Rift Valley Region',
            'counties_served': 'Nakuru, Eldoret, Kericho, Bomet, Narok',
            'headquarters_location': 'Nakuru',
            'registration_number': 'CS/005/2021',
            'is_active': True,
            'bodaboda_focused': True,
            'min_loan_amount': 10000,
            'max_loan_amount': 550000,
            'interest_rate_min': 14.0,
            'interest_rate_max': 21.0,
        }
    ]
    
    for sacco_data in saccos_data:
        sacco, created = SaccoProvider.objects.get_or_create(
            sacco_code=sacco_data['sacco_code'],
            defaults=sacco_data
        )
        if created:
            print(f"✅ Created SACCO: {sacco.name}")
        else:
            print(f"📋 SACCO already exists: {sacco.name}")

def create_sample_banks():
    """Create sample bank providers"""
    banks_data = [
        {
            'name': 'Kenya Commercial Bank',
            'bank_code': 'KCB',
            'phone_number': '+254711087000',
            'email': 'contactcentre@kcb.co.ke',
            'website': 'https://ke.kcbgroup.com',
            'physical_address': 'Kencom House, Moi Avenue, Nairobi',
            'is_active': True,
            'bodaboda_friendly': True,
            'min_loan_amount': 50000,
            'max_loan_amount': 2000000,
            'interest_rate_min': 15.0,
            'interest_rate_max': 25.0,
        },
        {
            'name': 'Equity Bank',
            'bank_code': 'EQT',
            'phone_number': '+254763000000',
            'email': 'info@equitybank.co.ke',
            'website': 'https://equitybank.co.ke',
            'physical_address': 'Equity Centre, Hospital Road, Nairobi',
            'is_active': True,
            'bodaboda_friendly': True,
            'min_loan_amount': 30000,
            'max_loan_amount': 1500000,
            'interest_rate_min': 14.0,
            'interest_rate_max': 24.0,
        },
        {
            'name': 'Co-operative Bank',
            'bank_code': 'COOP',
            'phone_number': '+254711049000',
            'email': 'customercare@co-opbank.co.ke',
            'website': 'https://www.co-opbank.co.ke',
            'physical_address': 'Co-op Bank House, Haile Selassie Avenue, Nairobi',
            'is_active': True,
            'bodaboda_friendly': True,
            'min_loan_amount': 25000,
            'max_loan_amount': 1000000,
            'interest_rate_min': 16.0,
            'interest_rate_max': 26.0,
        }
    ]
    
    for bank_data in banks_data:
        bank, created = BankProvider.objects.get_or_create(
            bank_code=bank_data['bank_code'],
            defaults=bank_data
        )
        if created:
            print(f"✅ Created Bank: {bank.name}")
        else:
            print(f"📋 Bank already exists: {bank.name}")

if __name__ == "__main__":
    print("🏦 Creating sample financial providers...")
    create_sample_saccos()
    create_sample_banks()
    print("✨ Sample data creation completed!")
