from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html

from .models import *


admin.site.register(Designation)
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(PersonalInformation)
admin.site.register(Branch)
admin.site.register(RequiredDocument)
admin.site.register(Immigration)
admin.site.register(BankDetails)
admin.site.register(EmployeeAttendence)
admin.site.register(LeaveMaster)
admin.site.register(LeaveApplication)
admin.site.register(Holiday)