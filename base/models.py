from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import nanoid
import os
from django_countries.fields import CountryField
from django.core.validators import RegexValidator
from .constants import STATE_CHOICES



def generate_unique_id():
    return nanoid.generate(size=25)


def get_upload_path(instance,filename):
    return os.path.join('Documents/' +  str(instance.employee.user.username),filename)
# Create your models here.

class Branch(models.Model):
    id = models.CharField(default=generate_unique_id,primary_key=True,editable=False,max_length=25)
    branch_name = models.CharField(max_length=100,unique=True)
    branch_code = models.CharField(max_length=100,unique=True)
    address = models.CharField(max_length=200,blank=True,null=True)
    tehsil = models.CharField(max_length=100,blank=True,null=True)
    district = models.CharField(max_length=100,blank=True,null=True)
    city = models.CharField(max_length=50,blank=True,null=True)
    state = models.CharField(max_length=50,choices=STATE_CHOICES,blank=True,null=True)
    country = CountryField(blank_label="(select country)")
    status = models.BooleanField()

    def __str__(self):
        return self.branch_name
    


class Designation(models.Model):
    id = models.CharField(max_length=25,primary_key=True,default=generate_unique_id,editable=False)
    designation_name = models.CharField(max_length=100,unique=True)
    designation_code = models.CharField(max_length=5,unique=True,blank=True,null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.designation_name
    
class Department(models.Model):
    id = models.CharField(max_length=25,primary_key=True,default=generate_unique_id,editable=False)
    department_name = models.CharField(max_length=100,unique=True)
    department_code = models.CharField(max_length=5,unique=True,blank=True,null=True)
    status = models.BooleanField(default=True)
    

    def __str__(self):
        return self.department_name
    

class Employee(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        
    ]
    SHIFT_CHOICES = [
        ('General', 'General'),
        ('UNICEF', 'UNICEF'),
        
    ]

    EMPLOYEE_TYPE_CHOICES = [
        ('Permanent','Permanent')
    ]

    GRADE_CHOICES = [
        ('Employee','Employee'),
        ('Consultant','Consultant'),
        ('UNF Employee','UNF Employee'),
        ('UNF Supervisor','UNF Supervisor'),
    ]

    id = models.CharField(max_length=25,primary_key=True,default=generate_unique_id,editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE,editable=False)
    employee_code = models.CharField(max_length=20,unique=True,null=True,blank=True)
    
    middle_name = models.CharField(max_length=100,blank=True,null=True)
   
    official_email= models.CharField(max_length=100, blank=True , null=True , unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    punching_code = models.IntegerField(unique=True , null=True , blank=True)
    date_of_joining = models.DateField(null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL,null=True,blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True,blank=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL,null=True,blank=True)
    employee_type = models.CharField(max_length=100, choices=EMPLOYEE_TYPE_CHOICES)
    shift = models.CharField(max_length=100, choices=SHIFT_CHOICES)
    grade = models.CharField(max_length=100, choices=GRADE_CHOICES)
    reporting_manager = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='reportees'
    )
    ctc = models.CharField(max_length=20,null=True,blank=True)
    gross_salary = models.CharField(max_length=20,null=True,blank=True)
    basic_salary = models.CharField(max_length=20,null=True,blank=True)

    

    def __str__(self):
        return self.user.username
    


    

class PersonalInformation(models.Model):

    MARITAL_STATUS_CHOICES = (
        ('Single' , 'Single'),
        ('Married' , 'Married'),

    )

    CASTE_CATEGORY_CHOICES = (
        ('General','General'),
        ('SC','SC'),
        ('ST','ST'),
        ('OBC','OBC'),
    )

    BLOOD_GROUP_CHOICES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )
     
    id = models.CharField(max_length=25,primary_key=True,default=generate_unique_id,editable=False)
    employee = models.OneToOneField(Employee,on_delete=models.CASCADE,editable=False)
    father_name = models.CharField(max_length=100,blank=True,null=True)
    mother_name = models.CharField(max_length=100,blank=True,null=True)
    mobile_no = models.CharField(max_length=10,unique=True,blank=True,null=True)
    blood_group = models.CharField(max_length=10,choices=BLOOD_GROUP_CHOICES,blank=True,null=True)
    nationality = models.CharField(max_length=10,blank=True,null=True)
    cast_category = models.CharField(choices=CASTE_CATEGORY_CHOICES,max_length=20,blank=True,null=True)
    marital_status = models.CharField(choices=MARITAL_STATUS_CHOICES,max_length=20,blank=True,null=True)
    aadhaar_card_no = models.CharField(max_length=12,null=True,blank=True,unique=True)
    pancard_no = models.CharField(max_length=10,null=True,blank=True,unique=True)
    address = models.CharField(max_length=200,blank=True,null=True)
    tehsil = models.CharField(max_length=100,blank=True,null=True)
    district = models.CharField(max_length=100,blank=True,null=True)
    city = models.CharField(max_length=50,blank=True,null=True)
    state = models.CharField(max_length=50,choices=STATE_CHOICES,blank=True,null=True)
    country =  CountryField(blank_label="select country",null=True,blank=True)
    pincode = models.CharField(max_length=10,blank=True,null=True)


    def __str__(self):
        return self.employee.user.username
    


class RequiredDocument(models.Model):
    
    DOCUMENT_CHOICES = (
        ('Aadhar Card','Aadhar Card'),
        ('Cancelled Cheque/Bank Passbook','Cancelled Cheque/Bank Passbook'),
        ('CV/Resume','CV/Resume'),
        ('Educational Certificates','Educational Certificates'),
        ('Experience/Employment Documents','Experience/Employment Documents'),
        ('Inductus Offer/Appointment Letter','Inductus Offer/Appointment Letter'),
        ('Other/All Documents','Other/All Documents'),
        ('PAN Card','PAN Card'),
        ('Salary Proof-Salary Slip/Bank Statement','Salary Proof-Salary Slip/Bank Statement'),
    )


    id = models.CharField(max_length=25,primary_key=True,default=generate_unique_id,editable=False)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,editable=False)
    document_type = models.CharField(max_length=100,choices=DOCUMENT_CHOICES,blank=True,null=True)
    document = models.FileField(upload_to=get_upload_path)
    comments = models.CharField(max_length=100,null=True,blank=True)
    date_of_expiry = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.employee.user.username
    


class Immigration(models.Model):
    IMMI_CHOICES = (
        ('Passport' , 'Passport'),
        ('Visa' , 'Visa'),
    )
    id = models.CharField(max_length=25,primary_key=True,default=generate_unique_id,editable=False)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,editable=False)
    document_type = models.CharField(max_length=100,choices=IMMI_CHOICES,blank=True,null=True)
    passport_or_visa_no = models.CharField(max_length=50)
    issue_date = models.DateField()
    date_of_expiry = models.DateField()
    citizenship = CountryField(blank_label="(select country)")
    comments = models.CharField(max_length=100,null=True,blank=True) 
    document = models.FileField(upload_to=get_upload_path)

    def __str__(self):
        return self.employee.user.username
    
class BankDetails(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE) 
    id = models.CharField(max_length=25,primary_key=True,default=generate_unique_id,editable=False)
    BANK_CHOICES = (
        ('HDFC', 'HDFC Bank'),
        ('ICICI', 'ICICI Bank'),
        ('SBI', 'State Bank of India'),
        ('Axis', 'Axis Bank'),
        ('Kotak', 'Kotak Mahindra Bank'),
        ('BOB', 'Bank of Baroda'),
        ('PNB', 'Punjab National Bank'),
        ('Other' , 'Other')
    )
   
    bank_name = models.CharField(max_length=100, choices=BANK_CHOICES)
    account_holder_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    IFSC_regex = RegexValidator(regex=r'^[A-Za-z]{4}\d{7}$', message="IFSC code must be in valid format.")
    IFSC_code = models.CharField(max_length=11, validators=[IFSC_regex])
    branch_name = models.CharField(max_length=255)
    branch_address = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.employee}'s Bank Details"
    


class Attendance(models.Model):
    id = models.CharField(max_length=25,primary_key=True,default=generate_unique_id,editable=False)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    in_Time = models.TimeField(blank=True,null=True)
    out_Time = models.TimeField(blank=True,null=True)
    date = models.DateField(blank=True,null=True)
    in_Location = models.CharField(max_length=200,null=True,blank=True)
    out_Location = models.CharField(max_length=200,null=True,blank=True)
    status = models.CharField(max_length=20,blank=True,null=True)

    def __str__(self):
        return f"{self.employee.user.username}'s Attendance" 
    
    @classmethod
    def mark_attendance(cls, employee, date, status):
        attendance, created = cls.objects.get_or_create(employee=employee, date=date)
        attendance.status = status
        attendance.save()
    

class LeaveMaster(models.Model):
    id = models.CharField(max_length=25,primary_key=True,default=generate_unique_id,editable=False)
    leave_name = models.CharField(max_length=50 , unique=True)
    leave_code = models.CharField(max_length=5,null=True,blank=True,unique=True)
    paid_leave = models.BooleanField(default=False)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.leave_name

class LeaveApplication(models.Model):

    id = models.CharField(max_length=25,primary_key=True,default=generate_unique_id,editable=False)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    leave_name = models.ForeignKey(LeaveMaster,on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    period = models.SmallIntegerField(default=0)
    reason = models.CharField(max_length=200,blank=True,null=True)
    status = models.CharField(max_length=50,default="Pending",blank=True,null=True)

    def __str__(self):
        return self.employee.user.username
    
class Holiday(models.Model):

    HOLIDAY_CHOICES = (
        ('National','National'),
        ('Festival' , 'Festival')
    )

    id = models.CharField(max_length=25,primary_key=True,default=generate_unique_id,editable=False)
    holiday_name = models.CharField(max_length=50)
    state = models.CharField(max_length=50,choices=STATE_CHOICES,blank=True,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
    holiday_date = models.DateField()
    holiday_category = models.CharField(max_length=50,choices=HOLIDAY_CHOICES)
    

    def __str__(self):
        return self.holiday_name


    
@receiver(post_save, sender=User)
def create_employee(sender, instance, created, **kwargs):
    if created and not instance.is_staff and not instance.is_superuser:
        Employee.objects.create(user=instance)





    


