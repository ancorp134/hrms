# urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('employee/login/', EmployeeLoginView.as_view(), name='employee-login'),
    path('employee/profile/', EmployeeInfo.as_view(), name='employee-info'),
    path('employee/attendance/',EmployeeAttendence.as_view(),name='employee-attendence')
]
