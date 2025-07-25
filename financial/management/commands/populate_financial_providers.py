"""
Management command to populate comprehensive boda boda-focused financial providers
"""
from django.core.management.base import BaseCommand
from decimal import Decimal
from financial.models import SaccoProvider, BankProvider

class Command(BaseCommand):
    help = 'Populate comprehensive financial providers (SACCOs and Banks) for boda boda riders'

    def handle(self, *args, **options):
        self.stdout.write("🏦 Populating Comprehensive Financial Providers for Boda Boda Riders...")
        self.stdout.write("=" * 70)
        
        self.populate_boda_boda_saccos()
        self.populate_boda_boda_friendly_banks()
        
        self.stdout.write("\n✅ Financial providers population completed!")
    
    def populate_boda_boda_saccos(self):
        """Populate comprehensive boda boda-focused SACCOs"""
        self.stdout.write("\n🏍️ Creating Boda Boda SACCOs...")
        
        sacco_data = [
            # PREMIER BODA BODA SACCOs (Direct Focus)
            {
                'name': 'Bodaboda Riders SACCO Kenya Limited',
                'sacco_code': 'BRSK001',
                'phone_number': '+254700123001',
                'email': 'info@bodabodariderssacco.co.ke',
                'physical_address': 'Nairobi CBD, Haile Selassie Avenue',
                'coverage_area': 'Nationwide',
                'counties_served': 'All 47 Counties',
                'headquarters_location': 'Nairobi',
                'min_loan_amount': Decimal('10000'),
                'max_loan_amount': Decimal('800000'),
                'interest_rate_min': Decimal('12.0'),
                'interest_rate_max': Decimal('18.0'),
                'max_repayment_period_months': 48,
                'minimum_savings_period': 3,
                'minimum_guarantors': 2,
                'registration_number': 'CS/KE/BRSK/001/2024',
                'member_count': 15000,
                'asset_value': Decimal('2500000000'),
                'description': '⭐ Premier nationwide SACCO exclusively for boda boda riders - motorcycle loans, insurance, emergency support',
                'bodaboda_focused': True,
                'target_demographic': 'Motorcycle Taxi Operators',
                'application_fee': Decimal('500'),
                'processing_time_days': 5,
            },
            {
                'name': 'Kenya Motorcycle Transport SACCO',
                'sacco_code': 'KMTS002',
                'phone_number': '+254700123002',
                'email': 'loans@motorcycletransport.co.ke',
                'physical_address': 'Mombasa Road, Industrial Area',
                'coverage_area': 'National',
                'counties_served': 'All 47 Counties',
                'headquarters_location': 'Nairobi',
                'min_loan_amount': Decimal('15000'),
                'max_loan_amount': Decimal('1200000'),
                'interest_rate_min': Decimal('10.5'),
                'interest_rate_max': Decimal('16.0'),
                'max_repayment_period_months': 60,
                'minimum_savings_period': 6,
                'minimum_guarantors': 2,
                'registration_number': 'CS/KE/KMTS/002/2023',
                'member_count': 25000,
                'asset_value': Decimal('4200000000'),
                'description': '⭐ National motorcycle transport SACCO - comprehensive financing for riders and bikes',
                'bodaboda_focused': True,
                'target_demographic': 'Professional Motorcycle Operators',
                'application_fee': Decimal('1000'),
                'processing_time_days': 7,
            },
            
            # REGIONAL BODA BODA SACCOs
            {
                'name': 'Central Kenya Bodaboda SACCO',
                'sacco_code': 'CKBS003',
                'phone_number': '+254700123003',
                'email': 'info@centralbodaboda.co.ke',
                'physical_address': 'Nyeri Town, Central Province',
                'coverage_area': 'Central Region',
                'counties_served': 'Kiambu, Nyeri, Murang\'a, Kirinyaga, Nyandarua',
                'headquarters_location': 'Nyeri',
                'min_loan_amount': Decimal('5000'),
                'max_loan_amount': Decimal('500000'),
                'interest_rate_min': Decimal('14.0'),
                'interest_rate_max': Decimal('20.0'),
                'max_repayment_period_months': 36,
                'minimum_savings_period': 3,
                'minimum_guarantors': 2,
                'registration_number': 'CS/KE/CKBS/003/2022',
                'member_count': 8500,
                'asset_value': Decimal('850000000'),
                'description': '📍 Central Kenya boda boda riders cooperative - coffee belt motorcycle financing',
                'bodaboda_focused': True,
                'target_demographic': 'Highland Region Riders',
                'application_fee': Decimal('300'),
                'processing_time_days': 3,
            },
            {
                'name': 'Coast Piki Piki Riders SACCO',
                'sacco_code': 'CPRS004',
                'phone_number': '+254700123004',
                'email': 'info@coastpikipiki.co.ke',
                'physical_address': 'Mombasa, Digo Road',
                'coverage_area': 'Coastal Region',
                'counties_served': 'Mombasa, Kilifi, Kwale, Tana River, Lamu, Taita Taveta',
                'headquarters_location': 'Mombasa',
                'min_loan_amount': Decimal('8000'),
                'max_loan_amount': Decimal('600000'),
                'interest_rate_min': Decimal('13.0'),
                'interest_rate_max': Decimal('19.0'),
                'max_repayment_period_months': 42,
                'minimum_savings_period': 2,
                'minimum_guarantors': 2,
                'registration_number': 'CS/KE/CPRS/004/2021',
                'member_count': 12000,
                'asset_value': Decimal('1800000000'),
                'description': '🏖️ Coastal region motorcycle riders SACCO - tourism and transport financing',
                'bodaboda_focused': True,
                'target_demographic': 'Coastal Transport Operators',
                'application_fee': Decimal('400'),
                'processing_time_days': 4,
            },
            {
                'name': 'Western Kenya Bodaboda Union SACCO',
                'sacco_code': 'WKBU005',
                'phone_number': '+254700123005',
                'email': 'loans@westernbodaboda.co.ke',
                'physical_address': 'Kakamega Town, Western Province',
                'coverage_area': 'Western Region',
                'counties_served': 'Kakamega, Bungoma, Busia, Vihiga, Siaya, Kisumu',
                'headquarters_location': 'Kakamega',
                'min_loan_amount': Decimal('7000'),
                'max_loan_amount': Decimal('450000'),
                'interest_rate_min': Decimal('15.0'),
                'interest_rate_max': Decimal('22.0'),
                'max_repayment_period_months': 36,
                'minimum_savings_period': 2,
                'minimum_guarantors': 2,
                'registration_number': 'CS/KE/WKBU/005/2020',
                'member_count': 18000,
                'asset_value': Decimal('2100000000'),
                'description': '🌾 Western Kenya boda boda union - agricultural belt motorcycle financing',
                'bodaboda_focused': True,
                'target_demographic': 'Agricultural Area Riders',
                'application_fee': Decimal('350'),
                'processing_time_days': 5,
            },
            
            # COUNTY-SPECIFIC BODA BODA SACCOs
            {
                'name': 'Nairobi Bodaboda Operators SACCO',
                'sacco_code': 'NBOS006',
                'phone_number': '+254700123006',
                'email': 'info@nairobibodaboda.co.ke',
                'physical_address': 'Nairobi CBD, Tom Mboya Street',
                'coverage_area': 'Nairobi County',
                'counties_served': 'Nairobi',
                'headquarters_location': 'Nairobi',
                'min_loan_amount': Decimal('20000'),
                'max_loan_amount': Decimal('1500000'),
                'interest_rate_min': Decimal('11.0'),
                'interest_rate_max': Decimal('17.0'),
                'max_repayment_period_months': 48,
                'minimum_savings_period': 6,
                'minimum_guarantors': 2,
                'registration_number': 'CS/KE/NBOS/006/2019',
                'member_count': 22000,
                'asset_value': Decimal('5500000000'),
                'description': '🏙️ Capital city boda boda operators SACCO - urban motorcycle financing',
                'bodaboda_focused': True,
                'target_demographic': 'Urban Professional Riders',
                'application_fee': Decimal('800'),
                'processing_time_days': 7,
            },
            {
                'name': 'Nakuru Transport Workers SACCO',
                'sacco_code': 'NTWS007',
                'phone_number': '+254700123007',
                'email': 'support@nakurutransport.co.ke',
                'physical_address': 'Nakuru Town, Kenyatta Avenue',
                'coverage_area': 'Nakuru County',
                'counties_served': 'Nakuru',
                'headquarters_location': 'Nakuru',
                'min_loan_amount': Decimal('12000'),
                'max_loan_amount': Decimal('800000'),
                'interest_rate_min': Decimal('13.5'),
                'interest_rate_max': Decimal('18.5'),
                'max_repayment_period_months': 36,
                'minimum_savings_period': 3,
                'minimum_guarantors': 2,
                'registration_number': 'CS/KE/NTWS/007/2021',
                'member_count': 9500,
                'asset_value': Decimal('1200000000'),
                'description': '📍 Rift Valley transport workers including boda boda financing',
                'bodaboda_focused': True,
                'target_demographic': 'Rift Valley Transport Workers',
                'application_fee': Decimal('450'),
                'processing_time_days': 4,
            },
            
            # SPECIALIZED BODA BODA SACCOs
            {
                'name': 'Youth Bodaboda Entrepreneurs SACCO',
                'sacco_code': 'YBES008',
                'phone_number': '+254700123008',
                'email': 'youth@bodabodaentrepreneurs.co.ke',
                'physical_address': 'Eldoret Town, Uganda Road',
                'coverage_area': 'Nationwide',
                'counties_served': 'Focus on Youth Demographics Nationwide',
                'headquarters_location': 'Eldoret',
                'min_loan_amount': Decimal('5000'),
                'max_loan_amount': Decimal('300000'),
                'interest_rate_min': Decimal('12.0'),
                'interest_rate_max': Decimal('16.0'),
                'max_repayment_period_months': 24,
                'minimum_savings_period': 1,
                'minimum_guarantors': 1,
                'registration_number': 'CS/KE/YBES/008/2023',
                'member_count': 11000,
                'asset_value': Decimal('650000000'),
                'description': '🎯 Youth-focused boda boda entrepreneurship SACCO - starter motorcycle loans',
                'bodaboda_focused': True,
                'target_demographic': 'Youth Entrepreneurs (18-35)',
                'application_fee': Decimal('200'),
                'processing_time_days': 2,
            },
            {
                'name': 'Women Bodaboda Empowerment SACCO',
                'sacco_code': 'WBES009',
                'phone_number': '+254700123009',
                'email': 'women@bodabodaempowerment.co.ke',
                'physical_address': 'Kisumu City, Oginga Odinga Street',
                'coverage_area': 'National',
                'counties_served': 'Women-focused Programs Nationwide',
                'headquarters_location': 'Kisumu',
                'min_loan_amount': Decimal('3000'),
                'max_loan_amount': Decimal('250000'),
                'interest_rate_min': Decimal('10.0'),
                'interest_rate_max': Decimal('15.0'),
                'max_repayment_period_months': 30,
                'minimum_savings_period': 1,
                'minimum_guarantors': 1,
                'registration_number': 'CS/KE/WBES/009/2022',
                'member_count': 5500,
                'asset_value': Decimal('320000000'),
                'description': '👩 Women empowerment through motorcycle transport - female rider support',
                'bodaboda_focused': True,
                'target_demographic': 'Women Motorcycle Operators',
                'application_fee': Decimal('150'),
                'processing_time_days': 3,
            },
            
            # MULTI-MODAL TRANSPORT SACCOs (Including Boda Boda)
            {
                'name': 'Highway Transport Operators SACCO',
                'sacco_code': 'HTOS010',
                'phone_number': '+254700123010',
                'email': 'info@highwaytransport.co.ke',
                'physical_address': 'Thika Town, Garissa Road',
                'coverage_area': 'Highway Corridors',
                'counties_served': 'Major Highway Towns and Routes',
                'headquarters_location': 'Thika',
                'min_loan_amount': Decimal('10000'),
                'max_loan_amount': Decimal('2000000'),
                'interest_rate_min': Decimal('14.0'),
                'interest_rate_max': Decimal('20.0'),
                'max_repayment_period_months': 60,
                'minimum_savings_period': 6,
                'minimum_guarantors': 2,
                'registration_number': 'CS/KE/HTOS/010/2018',
                'member_count': 13500,
                'asset_value': Decimal('3200000000'),
                'description': '🛣️ Highway transport operators including boda boda feeder services',
                'bodaboda_focused': True,
                'target_demographic': 'Highway Corridor Transport',
                'application_fee': Decimal('600'),
                'processing_time_days': 8,
            },
            
            # TECHNOLOGY-ENABLED BODA BODA SACCOs
            {
                'name': 'Digital Bodaboda Platform SACCO',
                'sacco_code': 'DBPS011',
                'phone_number': '+254700123011',
                'email': 'digital@bodabodaplatform.co.ke',
                'physical_address': 'Nairobi, Westlands Tech Hub',
                'coverage_area': 'Urban Centers',
                'counties_served': 'Nairobi, Mombasa, Kisumu, Nakuru, Eldoret',
                'headquarters_location': 'Nairobi',
                'min_loan_amount': Decimal('15000'),
                'max_loan_amount': Decimal('1000000'),
                'interest_rate_min': Decimal('9.5'),
                'interest_rate_max': Decimal('14.0'),
                'max_repayment_period_months': 36,
                'minimum_savings_period': 3,
                'minimum_guarantors': 1,
                'registration_number': 'CS/KE/DBPS/011/2024',
                'member_count': 7800,
                'asset_value': Decimal('1100000000'),
                'description': '📱 Technology-enabled boda boda platform SACCO - app-based riders',
                'bodaboda_focused': True,
                'target_demographic': 'Tech-Savvy Urban Riders',
                'application_fee': Decimal('300'),
                'processing_time_days': 2,
                'online_application_available': True,
            },
        ]
        
        created_count = 0
        for sacco_info in sacco_data:
            sacco, created = SaccoProvider.objects.get_or_create(
                name=sacco_info['name'],
                defaults=sacco_info
            )
            
            if created:
                created_count += 1
                # Determine marker based on description
                if "⭐" in sacco_info['description']:
                    marker = "⭐"
                elif "🎯" in sacco_info['description']:
                    marker = "🎯"
                elif "👩" in sacco_info['description']:
                    marker = "👩"
                elif "📍" in sacco_info['description']:
                    marker = "📍"
                elif "📱" in sacco_info['description']:
                    marker = "📱"
                else:
                    marker = "🏦"
                
                self.stdout.write(f"{marker} Created: {sacco_info['name']}")
        
        total_saccos = SaccoProvider.objects.count()
        self.stdout.write(f"\n📊 SACCO Summary: {total_saccos} total, {created_count} new")
    
    def populate_boda_boda_friendly_banks(self):
        """Populate banks that offer boda boda financing"""
        self.stdout.write("\n🏛️ Creating Boda Boda-Friendly Banks...")
        
        bank_data = [
            # MAJOR COMMERCIAL BANKS WITH BODA BODA PRODUCTS
            {
                'name': 'Kenya Commercial Bank (KCB)',
                'bank_code': 'KCB001',
                'phone_number': '+254711087000',
                'email': 'customercare@kcbgroup.com',
                'website': 'https://ke.kcbgroup.com',
                'head_office_address': 'KCB Centre, Upper Hill, Nairobi',
                'swift_code': 'KCBLKENX',
                'license_number': 'CBK/B/001',
                'total_branches': 250,
                'counties_with_branches': 'All 47 Counties',
                'motorcycle_loan_min': Decimal('50000'),
                'motorcycle_loan_max': Decimal('2000000'),
                'business_loan_min': Decimal('10000'),
                'business_loan_max': Decimal('5000000'),
                'motorcycle_loan_rate_min': Decimal('16.0'),
                'motorcycle_loan_rate_max': Decimal('22.0'),
                'business_loan_rate_min': Decimal('18.0'),
                'business_loan_rate_max': Decimal('25.0'),
                'motorcycle_loan_max_term': 60,
                'business_loan_max_term': 36,
                'minimum_income_requirement': Decimal('15000'),
                'application_fee': Decimal('2000'),
                'processing_time_days': 14,
                'approval_rate': Decimal('65.0'),
                'ussd_banking': '*522#',
                'description': '🏛️ Largest bank in Kenya with specialized motorcycle financing products',
            },
            {
                'name': 'Equity Bank Kenya',
                'bank_code': 'EQB002',
                'phone_number': '+254763000000',
                'email': 'info@equitybank.co.ke',
                'website': 'https://equitybank.co.ke',
                'head_office_address': 'Equity Centre, Upper Hill, Nairobi',
                'swift_code': 'EQBLKENA',
                'license_number': 'CBK/B/002',
                'total_branches': 190,
                'counties_with_branches': 'All 47 Counties',
                'motorcycle_loan_min': Decimal('30000'),
                'motorcycle_loan_max': Decimal('1500000'),
                'business_loan_min': Decimal('5000'),
                'business_loan_max': Decimal('3000000'),
                'motorcycle_loan_rate_min': Decimal('14.5'),
                'motorcycle_loan_rate_max': Decimal('20.0'),
                'business_loan_rate_min': Decimal('16.5'),
                'business_loan_rate_max': Decimal('23.0'),
                'motorcycle_loan_max_term': 48,
                'business_loan_max_term': 36,
                'minimum_income_requirement': Decimal('12000'),
                'application_fee': Decimal('1500'),
                'processing_time_days': 10,
                'approval_rate': Decimal('70.0'),
                'ussd_banking': '*247#',
                'description': '🏛️ Leading SME bank with boda boda entrepreneur focus',
            },
            {
                'name': 'Cooperative Bank of Kenya',
                'bank_code': 'COB003',
                'phone_number': '+254711049000',
                'email': 'customercare@co-opbank.co.ke',
                'website': 'https://www.co-opbank.co.ke',
                'head_office_address': 'Co-operative House, Upper Hill, Nairobi',
                'swift_code': 'KCOOKENA',
                'license_number': 'CBK/B/003',
                'total_branches': 140,
                'counties_with_branches': 'All 47 Counties',
                'motorcycle_loan_min': Decimal('40000'),
                'motorcycle_loan_max': Decimal('1800000'),
                'business_loan_min': Decimal('8000'),
                'business_loan_max': Decimal('4000000'),
                'motorcycle_loan_rate_min': Decimal('15.0'),
                'motorcycle_loan_rate_max': Decimal('21.0'),
                'business_loan_rate_min': Decimal('17.0'),
                'business_loan_rate_max': Decimal('24.0'),
                'motorcycle_loan_max_term': 54,
                'business_loan_max_term': 42,
                'minimum_income_requirement': Decimal('13000'),
                'application_fee': Decimal('1800'),
                'processing_time_days': 12,
                'approval_rate': Decimal('68.0'),
                'ussd_banking': '*667#',
                'description': '🏛️ Cooperative-focused bank supporting transport cooperatives',
            },
            
            # SPECIALIZED SME AND MICROFINANCE BANKS
            {
                'name': 'Family Bank Limited',
                'bank_code': 'FAM004',
                'phone_number': '+254711056000',
                'email': 'customercare@familybank.co.ke',
                'website': 'https://www.familybank.co.ke',
                'head_office_address': 'Family Bank Tower, Muindi Mbingu Street, Nairobi',
                'swift_code': 'FABLKENA',
                'license_number': 'CBK/B/004',
                'total_branches': 85,
                'counties_with_branches': '35 Counties',
                'motorcycle_loan_min': Decimal('25000'),
                'motorcycle_loan_max': Decimal('1200000'),
                'business_loan_min': Decimal('10000'),
                'business_loan_max': Decimal('2500000'),
                'motorcycle_loan_rate_min': Decimal('16.5'),
                'motorcycle_loan_rate_max': Decimal('23.0'),
                'business_loan_rate_min': Decimal('18.5'),
                'business_loan_rate_max': Decimal('26.0'),
                'motorcycle_loan_max_term': 42,
                'business_loan_max_term': 30,
                'minimum_income_requirement': Decimal('10000'),
                'application_fee': Decimal('1200'),
                'processing_time_days': 8,
                'approval_rate': Decimal('72.0'),
                'ussd_banking': '*434#',
                'description': '🏛️ SME-focused bank with flexible motorcycle financing',
            },
            {
                'name': 'KWFT Bank (Kenya Women Microfinance Bank)',
                'bank_code': 'KWF005',
                'phone_number': '+254709986000',
                'email': 'info@kwftbank.com',
                'website': 'https://www.kwftbank.com',
                'head_office_address': 'KWFT Centre, Nairobi',
                'swift_code': 'KWMFKENA',
                'license_number': 'CBK/MFB/005',
                'total_branches': 45,
                'counties_with_branches': '25 Counties',
                'motorcycle_loan_min': Decimal('15000'),
                'motorcycle_loan_max': Decimal('800000'),
                'business_loan_min': Decimal('5000'),
                'business_loan_max': Decimal('1500000'),
                'motorcycle_loan_rate_min': Decimal('18.0'),
                'motorcycle_loan_rate_max': Decimal('25.0'),
                'business_loan_rate_min': Decimal('20.0'),
                'business_loan_rate_max': Decimal('28.0'),
                'motorcycle_loan_max_term': 36,
                'business_loan_max_term': 24,
                'minimum_income_requirement': Decimal('8000'),
                'application_fee': Decimal('800'),
                'processing_time_days': 5,
                'approval_rate': Decimal('75.0'),
                'description': '👩 Women-focused microfinance bank supporting female riders',
            },
            
            # DIGITAL AND MOBILE BANKS
            {
                'name': 'NCBA Bank Kenya',
                'bank_code': 'NCB006',
                'phone_number': '+254711056000',
                'email': 'contactcentre@ncbagroup.com',
                'website': 'https://ke.ncbagroup.com',
                'head_office_address': 'NCBA Centre, Upper Hill, Nairobi',
                'swift_code': 'CBAFKENA',
                'license_number': 'CBK/B/006',
                'total_branches': 100,
                'counties_with_branches': '40 Counties',
                'motorcycle_loan_min': Decimal('35000'),
                'motorcycle_loan_max': Decimal('1600000'),
                'business_loan_min': Decimal('12000'),
                'business_loan_max': Decimal('3500000'),
                'motorcycle_loan_rate_min': Decimal('15.5'),
                'motorcycle_loan_rate_max': Decimal('21.5'),
                'business_loan_rate_min': Decimal('17.5'),
                'business_loan_rate_max': Decimal('24.5'),
                'motorcycle_loan_max_term': 48,
                'business_loan_max_term': 36,
                'minimum_income_requirement': Decimal('14000'),
                'application_fee': Decimal('1600'),
                'processing_time_days': 10,
                'approval_rate': Decimal('69.0'),
                'ussd_banking': '*225#',
                'description': '🏛️ Digital-first bank with mobile motorcycle loan applications',
            },
            
            # AGRICULTURAL AND DEVELOPMENT BANKS
            {
                'name': 'Agricultural Finance Corporation (AFC)',
                'bank_code': 'AFC007',
                'phone_number': '+254709986000',
                'email': 'info@afc.co.ke',
                'website': 'https://www.afc.co.ke',
                'head_office_address': 'AFC House, Nairobi',
                'swift_code': 'AFCOKENA',
                'license_number': 'CBK/DFI/007',
                'total_branches': 35,
                'counties_with_branches': '30 Agricultural Counties',
                'motorcycle_loan_min': Decimal('20000'),
                'motorcycle_loan_max': Decimal('1000000'),
                'business_loan_min': Decimal('15000'),
                'business_loan_max': Decimal('2000000'),
                'motorcycle_loan_rate_min': Decimal('12.0'),
                'motorcycle_loan_rate_max': Decimal('18.0'),
                'business_loan_rate_min': Decimal('14.0'),
                'business_loan_rate_max': Decimal('20.0'),
                'motorcycle_loan_max_term': 60,
                'business_loan_max_term': 48,
                'minimum_income_requirement': Decimal('8000'),
                'application_fee': Decimal('1000'),
                'processing_time_days': 15,
                'approval_rate': Decimal('60.0'),
                'description': '🚜 Agricultural development bank supporting rural transport',
            },
            
            # ISLAMIC BANKS
            {
                'name': 'First Community Bank (Sharia-Compliant)',
                'bank_code': 'FCB008',
                'phone_number': '+254709000000',
                'email': 'info@fcb.co.ke',
                'website': 'https://www.fcb.co.ke',
                'head_office_address': 'First Community Bank Centre, Nairobi',
                'swift_code': 'FCBKKENA',
                'license_number': 'CBK/B/008',
                'total_branches': 25,
                'counties_with_branches': 'Coast, North Eastern, Nairobi',
                'motorcycle_loan_min': Decimal('30000'),
                'motorcycle_loan_max': Decimal('1200000'),
                'business_loan_min': Decimal('10000'),
                'business_loan_max': Decimal('2500000'),
                'motorcycle_loan_rate_min': Decimal('0.0'),  # Profit sharing model
                'motorcycle_loan_rate_max': Decimal('15.0'),
                'business_loan_rate_min': Decimal('0.0'),
                'business_loan_rate_max': Decimal('18.0'),
                'motorcycle_loan_max_term': 36,
                'business_loan_max_term': 30,
                'minimum_income_requirement': Decimal('12000'),
                'application_fee': Decimal('1500'),
                'processing_time_days': 12,
                'approval_rate': Decimal('65.0'),
                'description': '🕌 Sharia-compliant Islamic banking for Muslim boda boda operators',
            },
        ]
        
        created_count = 0
        for bank_info in bank_data:
            bank, created = BankProvider.objects.get_or_create(
                name=bank_info['name'],
                defaults=bank_info
            )
            
            if created:
                created_count += 1
                # Determine marker
                if "👩" in bank_info['description']:
                    marker = "👩"
                elif "🕌" in bank_info['description']:
                    marker = "🕌"
                elif "🚜" in bank_info['description']:
                    marker = "🚜"
                else:
                    marker = "🏛️"
                
                self.stdout.write(f"{marker} Created: {bank_info['name']}")
        
        total_banks = BankProvider.objects.count()
        self.stdout.write(f"\n📊 Bank Summary: {total_banks} total, {created_count} new")
        
        # Final summary
        total_saccos = SaccoProvider.objects.count()
        self.stdout.write(f"\n🎉 COMPREHENSIVE FINANCIAL PROVIDER SUMMARY:")
        self.stdout.write(f"   - 🏦 Total SACCOs: {total_saccos}")
        self.stdout.write(f"   - 🏛️ Total Banks: {total_banks}")
        self.stdout.write(f"   - 📍 Coverage: All 47 counties")
        self.stdout.write(f"   - 🏍️ Boda boda riders now have access to {total_saccos + total_banks} financial providers!")
        self.stdout.write(f"   - ⭐ = Premier Boda Boda SACCOs")
        self.stdout.write(f"   - 🎯 = Youth Focused")
        self.stdout.write(f"   - 👩 = Women Focused")
        self.stdout.write(f"   - 📱 = Technology Enabled")
        self.stdout.write(f"   - 🕌 = Islamic/Sharia Compliant")
        self.stdout.write(f"   - 🚜 = Agricultural/Rural Focus")
