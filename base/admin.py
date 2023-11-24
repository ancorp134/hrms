from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html

from .models import *




# Register your models here.
# class EmployeeAdmin(admin.ModelAdmin):

#     list_display = ("user","employee_code","first_name","last_name","branch","punching_code")
#     search_fields = ['employee_code',"first_name" , "last_name" , "branch"]
    
   
  
    



admin.site.register(Designation)
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(PersonalInformation)
admin.site.register(Branch)
admin.site.register(RequiredDocument)
