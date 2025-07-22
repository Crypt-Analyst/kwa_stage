#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bodaboda_welfare.settings')
django.setup()

from django.contrib.auth.models import User
from members.models import Member
from stages.models import Stage
from django.db import transaction

def test_member_creation():
    """Test creating a member to identify any issues"""
    print("Testing member creation...")
    
    # Get or create a test user
    try:
        user = User.objects.get(username='testuser@example.com')
        print(f"Found existing user: {user.email}")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='testuser@example.com',
            email='testuser@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        print(f"Created new user: {user.email}")
    
    # Get a stage
    try:
        stage = Stage.objects.first()
        if not stage:
            print("No stages found! Creating a test stage...")
            stage = Stage.objects.create(
                name='Test Stage',
                location='Test Location',
                county='Nairobi',
                is_active=True
            )
        print(f"Using stage: {stage.name}")
    except Exception as e:
        print(f"Error with stage: {e}")
        return
    
    # Try to create or update member
    try:
        with transaction.atomic():
            # Check if member already exists
            try:
                member = user.member
                print(f"Found existing member: {member.member_number}")
                # Update the member
                member.national_id = '12345678'
                member.phone_number = '+254712345678'
                member.stage = stage
                member.zone = 'Test Zone'
                member.sacco = 'Test SACCO'
                member.next_of_kin_name = 'Test Next of Kin'
                member.next_of_kin_relationship = 'spouse'
                member.next_of_kin_phone = '+254712345679'
                member.next_of_kin_id = '87654321'
                member.date_of_birth = '1990-01-01'
                member.address = 'Test Address, Nairobi'
                member.dependents_count = 2
                member.save()
                print("Member updated successfully!")
                
            except Member.DoesNotExist:
                print("Creating new member...")
                import random
                member_number = f"KWS{random.randint(1000, 9999)}"
                while Member.objects.filter(member_number=member_number).exists():
                    member_number = f"KWS{random.randint(1000, 9999)}"
                
                member = Member.objects.create(
                    user=user,
                    national_id='12345678',
                    phone_number='+254712345678',
                    stage=stage,
                    zone='Test Zone',
                    sacco='Test SACCO',
                    next_of_kin_name='Test Next of Kin',
                    next_of_kin_relationship='spouse',
                    next_of_kin_phone='+254712345679',
                    next_of_kin_id='87654321',
                    date_of_birth='1990-01-01',
                    address='Test Address, Nairobi',
                    member_number=member_number,
                    dependents_count=2
                )
                print(f"Member created successfully! Member Number: {member.member_number}")
            
            # Verify the member was saved
            saved_member = Member.objects.get(user=user)
            print(f"Verification - Member found in DB:")
            print(f"  - Name: {saved_member.full_name}")
            print(f"  - Member Number: {saved_member.member_number}")
            print(f"  - National ID: {saved_member.national_id}")
            print(f"  - Phone: {saved_member.phone_number}")
            print(f"  - Stage: {saved_member.stage.name}")
            print(f"  - Zone: {saved_member.zone}")
            print(f"  - Next of Kin: {saved_member.next_of_kin_name}")
            print(f"  - Dependents: {saved_member.dependents_count}")
            print(f"  - Date Created: {saved_member.created_at}")
            
            return True
            
    except Exception as e:
        print(f"Error creating/updating member: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_member_creation()
    if success:
        print("\n✅ Member creation test PASSED")
    else:
        print("\n❌ Member creation test FAILED")
