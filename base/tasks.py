# tasks.py in your app directory

from celery import shared_task
from datetime import date
from .models import Attendance, Employee
from time import sleep



@shared_task
def mark_absentees():
    sleep(10)
    today = date.today()
    employees = Employee.objects.all()
    
    for employee in employees:
        
        attendance_exists = Attendance.objects.filter(employee=employee, date=today).exists()

        if not attendance_exists:
            Attendance.mark_attendance(employee, today, 'Absent')
            
        
                
                
