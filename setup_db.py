"""
Helper script to set up the database and create initial data
Run this after migrations: python setup_db.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinic_appointment.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import DoctorProfile

User = get_user_model()

def create_sample_data():
    """Create sample users and doctor profiles for testing"""
    
    # Create admin user
    if not User.objects.filter(email='admin@clinic.com').exists():
        admin = User.objects.create_superuser(
            email='admin@clinic.com',
            username='admin',
            password='admin123',
            user_type='STAFF',
            first_name='Admin',
            last_name='User'
        )
        print(f"✓ Created admin user: {admin.email}")
    
    # Create sample doctors
    doctors_data = [
        {
            'email': 'dr.smith@clinic.com',
            'username': 'drsmith',
            'first_name': 'John',
            'last_name': 'Smith',
            'specialization': 'Cardiology',
            'bio': 'Experienced cardiologist with 15 years of practice.',
            'years_of_experience': 15,
            'consultation_fee': 150.00
        },
        {
            'email': 'dr.jones@clinic.com',
            'username': 'drjones',
            'first_name': 'Sarah',
            'last_name': 'Jones',
            'specialization': 'Pediatrics',
            'bio': 'Pediatric specialist focused on child healthcare.',
            'years_of_experience': 10,
            'consultation_fee': 120.00
        },
        {
            'email': 'dr.williams@clinic.com',
            'username': 'drwilliams',
            'first_name': 'Michael',
            'last_name': 'Williams',
            'specialization': 'Dermatology',
            'bio': 'Expert in skin care and dermatological treatments.',
            'years_of_experience': 12,
            'consultation_fee': 130.00
        }
    ]
    
    for doc_data in doctors_data:
        email = doc_data.pop('email')
        username = doc_data.pop('username')
        specialization = doc_data.pop('specialization')
        bio = doc_data.pop('bio')
        years = doc_data.pop('years_of_experience')
        fee = doc_data.pop('consultation_fee')
        
        if not User.objects.filter(email=email).exists():
            doctor = User.objects.create_user(
                email=email,
                username=username,
                password='doctor123',
                user_type='STAFF',
                **doc_data
            )
            
            DoctorProfile.objects.create(
                user=doctor,
                specialization=specialization,
                bio=bio,
                years_of_experience=years,
                consultation_fee=fee,
                is_available=True
            )
            print(f"✓ Created doctor: {doctor.email} ({specialization})")
    
    # Create sample patient
    if not User.objects.filter(email='patient@example.com').exists():
        patient = User.objects.create_user(
            email='patient@example.com',
            username='patient1',
            password='patient123',
            user_type='PATIENT',
            first_name='Test',
            last_name='Patient'
        )
        print(f"✓ Created patient: {patient.email}")
    
    print("\n✓ Sample data created successfully!")
    print("\nLogin credentials:")
    print("Admin: admin@clinic.com / admin123")
    print("Doctor: dr.smith@clinic.com / doctor123")
    print("Patient: patient@example.com / patient123")

if __name__ == '__main__':
    create_sample_data()

