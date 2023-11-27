from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import nanoid
import os
from django_countries.fields import CountryField
from django.core.validators import RegexValidator



def generate_unique_id():
    return nanoid.generate(size=25)


def get_upload_path(instance,filename):
    return os.path.join('Documents/' +  str(instance.employee.user.username),filename)
# Create your models here.

class Branch(models.Model):
    id = models.CharField(default=generate_unique_id,primary_key=True,editable=False,max_length=25)
    branch_name = models.CharField(max_length=100,unique=True)
    slug = models.CharField(max_length=100)

    def __str__(self):
        return self.branch_name
    


class Designation(models.Model):
    id = models.CharField(max_length=25,primary_key=True,default=generate_unique_id,editable=False)
    designation = models.CharField(max_length=100,unique=True)
    slug = models.CharField(max_length=100)

    def __str__(self):
        return self.designation
    
class Department(models.Model):
    id = models.CharField(max_length=25,primary_key=True,default=generate_unique_id,editable=False)
    department = models.CharField(max_length=100,unique=True)
    slug = models.CharField(max_length=100)

    

    def __str__(self):
        return self.department
    

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
    first_name = models.CharField(max_length=100 ,null=True,blank=True)
    middle_name = models.CharField(max_length=100,blank=True,null=True)
    last_name = models.CharField(max_length=100 , null=True,blank=True)
    email = models.CharField(max_length=100, null=True,blank=True , unique=True)
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

    STATE_CHOICES = (
        ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Arunachal Pradesh', 'Arunachal Pradesh'),
        ('Assam', 'Assam'),
        ('Bihar', 'Bihar'),
        ('Chandigarh', 'Chandigarh'),
        ('Chhattisgarh', 'Chhattisgarh'),
        ('Dadra and Nagar Haveli', 'Dadra and Nagar Haveli'),
        ('Daman and Diu', 'Daman and Diu'),
        ('Delhi', 'Delhi'),
        ('Goa', 'Goa'),
        ('Gujarat', 'Gujarat'),
        ('Haryana', 'Haryana'),
        ('Himachal Pradesh', 'Himachal Pradesh'),
        ('Jammu and Kashmir', 'Jammu and Kashmir'),
        ('Jharkhand', 'Jharkhand'),
        ('Karnataka', 'Karnataka'),
        ('Kerala', 'Kerala'),
        ('Lakshadweep', 'Lakshadweep'),
        ('Madhya Pradesh', 'Madhya Pradesh'),
        ('Maharashtra', 'Maharashtra'),
        ('Manipur', 'Manipur'),
        ('Meghalaya', 'Meghalaya'),
        ('Mizoram', 'Mizoram'),
        ('Nagaland', 'Nagaland'),
        ('Odisha', 'Odisha'),
        ('Puducherry', 'Puducherry'),
        ('Punjab', 'Punjab'),
        ('Rajasthan', 'Rajasthan'),
        ('Sikkim', 'Sikkim'),
        ('Tamil Nadu', 'Tamil Nadu'),
        ('Telangana', 'Telangana'),
        ('Tripura', 'Tripura'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('Uttarakhand', 'Uttarakhand'),
        ('West Bengal', 'West Bengal'),
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
    address = models.CharField(max_length=200,blank=True,null=True)
    tehsil = models.CharField(max_length=100,blank=True,null=True)
    district = models.CharField(max_length=100,blank=True,null=True)
    city = models.CharField(max_length=50,blank=True,null=True)
    state = models.CharField(max_length=50,choices=STATE_CHOICES,blank=True,null=True)
    country = models.CharField(max_length=50,blank=True,null=True)
    pincode = models.CharField(max_length=10,blank=True,null=True)
    nationality = models.CharField(max_length=10,blank=True,null=True)
    cast_category = models.CharField(max_length=20,blank=True,null=True)
    

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
    BANK_STATUS = (
        ('Primary' , 'Primary'),
        ('Secondary' , 'Secondary')
    )
    bank_name = models.CharField(max_length=100, choices=BANK_CHOICES)
    account_holder_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    IFSC_regex = RegexValidator(regex=r'^[A-Za-z]{4}\d{7}$', message="IFSC code must be in valid format.")
    IFSC_code = models.CharField(max_length=11, validators=[IFSC_regex])
    branch_name = models.CharField(max_length=255)
    branch_address = models.CharField(max_length=255)
    status = models.CharField(max_length=50,choices=BANK_STATUS)
    
    
    def __str__(self):
        return f"{self.employee}'s Bank Details"

    
@receiver(post_save, sender=User)
def create_employee(sender, instance, created, **kwargs):
    if created and not instance.is_staff and not instance.is_superuser:
        Employee.objects.create(user=instance)





    


