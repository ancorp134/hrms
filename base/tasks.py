# tasks.py in your app directory

from celery import shared_task
from datetime import date, datetime, time
from .models import Attendance, Employee
import logging

logger = logging.getLogger(__name__)

@shared_task
def mark_absentees():
    print("welcome............")
    today = date.today()
    employees = Employee.objects.all()
    logger.info(f"Processing attendance for {today}")
    for employee in employees:
        logger.info(f"Processing attendance for employee: {employee.name}")
        attendance_exists = Attendance.objects.filter(employee=employee, date=today).exists()

        if not attendance_exists:
            Attendance.mark_attendance(employee, today, 'Absent')
            
        else:
            attendance = Attendance.objects.get(employee=employee, date=today)
            if not attendance.check_in_time:
                attendance.check_in_time = datetime.now()  # Update check-in time if not set
                attendance.status = 'Present'
                attendance.save()
           
                
                
