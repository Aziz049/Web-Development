"""
Utility functions for calculating doctor availability and time slots
"""
from datetime import date, datetime, time, timedelta
from django.utils import timezone
from accounts.models import DoctorSchedule, DoctorProfile
from .models import Appointment


def get_available_time_slots(doctor_id, appointment_date, slot_duration_minutes=30):
    """
    Calculate available time slots for a doctor on a specific date.
    
    Args:
        doctor_id: Doctor's user ID
        appointment_date: Date to check availability for
        slot_duration_minutes: Duration of each time slot (default 30 minutes)
        
    Returns:
        list: List of available time slots as time objects
    """
    try:
        doctor = DoctorProfile.objects.get(user_id=doctor_id)
    except DoctorProfile.DoesNotExist:
        return []
    
    # Get day of week (0=Monday, 6=Sunday)
    day_of_week = appointment_date.weekday()
    
    # Get doctor's schedule for this day
    try:
        schedule = DoctorSchedule.objects.get(
            doctor=doctor,
            day_of_week=day_of_week,
            is_available=True
        )
    except DoctorSchedule.DoesNotExist:
        return []  # Doctor not available on this day
    
    # Get existing appointments for this date
    existing_appointments = Appointment.objects.filter(
        doctor_id=doctor_id,
        appointment_date=appointment_date
    ).exclude(status='CANCELLED')
    
    booked_times = {apt.appointment_time for apt in existing_appointments}
    
    # Generate time slots
    available_slots = []
    current_time = schedule.start_time
    end_time = schedule.end_time
    
    # If it's today, don't show past times
    today = date.today()
    if appointment_date == today:
        now = datetime.now().time()
        if current_time < now:
            # Round up to next slot
            current_hour = now.hour
            current_minute = now.minute
            # Round to next 30-minute slot
            if current_minute < 30:
                current_minute = 30
            else:
                current_hour += 1
                current_minute = 0
            current_time = time(current_hour, current_minute)
    
    while current_time < end_time:
        # Check if this slot is not booked
        if current_time not in booked_times:
            available_slots.append(current_time)
        
        # Move to next slot
        current_datetime = datetime.combine(date.today(), current_time)
        next_datetime = current_datetime + timedelta(minutes=slot_duration_minutes)
        current_time = next_datetime.time()
        
        # Safety check to prevent infinite loop
        if current_time <= schedule.start_time:
            break
    
    return available_slots


def is_time_slot_available(doctor_id, appointment_date, appointment_time):
    """
    Check if a specific time slot is available for booking.
    
    Args:
        doctor_id: Doctor's user ID
        appointment_date: Date to check
        appointment_time: Time to check
        
    Returns:
        bool: True if available, False otherwise
    """
    # Check if date is in the past
    if appointment_date < date.today():
        return False
    
    # Check if time is in the past for today
    if appointment_date == date.today():
        now = datetime.now().time()
        if appointment_time < now:
            return False
    
    # Check doctor's schedule
    try:
        doctor = DoctorProfile.objects.get(user_id=doctor_id)
        day_of_week = appointment_date.weekday()
        
        schedule = DoctorSchedule.objects.get(
            doctor=doctor,
            day_of_week=day_of_week,
            is_available=True
        )
        
        # Check if time is within schedule
        if not (schedule.start_time <= appointment_time < schedule.end_time):
            return False
        
    except (DoctorProfile.DoesNotExist, DoctorSchedule.DoesNotExist):
        return False
    
    # Check if slot is already booked
    is_booked = Appointment.objects.filter(
        doctor_id=doctor_id,
        appointment_date=appointment_date,
        appointment_time=appointment_time
    ).exclude(status='CANCELLED').exists()
    
    return not is_booked


def get_doctor_availability(doctor_id, start_date=None, end_date=None, days_ahead=30):
    """
    Get doctor's availability for a date range.
    
    Args:
        doctor_id: Doctor's user ID
        start_date: Start date (default: today)
        end_date: End date (default: start_date + days_ahead)
        days_ahead: Number of days to look ahead (default: 30)
        
    Returns:
        dict: Dictionary mapping dates to available time slots
    """
    if start_date is None:
        start_date = date.today()
    
    if end_date is None:
        end_date = start_date + timedelta(days=days_ahead)
    
    availability = {}
    current_date = start_date
    
    while current_date <= end_date:
        # Skip past dates
        if current_date >= date.today():
            slots = get_available_time_slots(doctor_id, current_date)
            if slots:
                availability[str(current_date)] = [slot.strftime('%H:%M') for slot in slots]
        
        current_date += timedelta(days=1)
    
    return availability

