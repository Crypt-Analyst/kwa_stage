from financial.models import SaccoProvider

# Create a simple SACCO for testing
sacco = SaccoProvider(
    name='Test Boda Boda SACCO',
    sacco_code='TEST001',
    phone_number='+254700000000',
    email='test@sacco.co.ke',
    physical_address='Test Address, Nairobi',
    coverage_area='Central Region',
    counties_served='Nairobi, Kiambu, Machakos',
    headquarters_location='Nairobi',
    registration_number='CS/TEST/2023',
    is_active=True,
    bodaboda_focused=True,
    description='Test SACCO for boda boda riders'
)
sacco.save()
print(f'Created SACCO: {sacco.name}')
