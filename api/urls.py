# urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('employee/login/', EmployeeLoginView.as_view(), name='employee-login'),
    path('employee/profile/', EmployeeInfo.as_view(), name='employee-info'),
    path('employee/attendance/',EmployeeAttendence.as_view(),name='employee-attendence'),
    path('employee/leave-application/',LeaveApplicationView.as_view(),name='leave-application'),
    path('employee/leave-application/<str:pk>/delete',deleteleave.as_view(),name='leave-delete'),
    path('employee/leave-application/<str:pk>/approve',approveleave.as_view(),name='approve-delete'),
    path('employee/leave-application/<str:pk>/reject',rejectleave.as_view(),name='reject-delete'),
]
