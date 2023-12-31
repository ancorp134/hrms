from django.contrib import admin
from django.urls import path,include
from base import views
from django.conf import settings
from django.conf.urls.static import static


handler404 = 'base.views.handler404'
handler500 = 'base.views.handler500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.LoginView,name='signin'),
    path('logout/',views.LogoutView,name='logout'),
    path('dashboard/',views.Dashboard,name='dashboard'),
    path('employees_profiles/',views.EmployeeView,name='employees'),
    path('job-master/branch-master/',views.BranchMaster,name='branch-master'),
    path('job-master/branch-master/<str:pk>/delete',views.deleteBranch,name="deletebranch"),
    path('job-master/branch-master/<str:pk>/edit',views.editBranch,name="editbranch"),
    path('job-master/department-master/',views.DepartmentMaster,name='department-master'),
    path('job-master/department-master/<str:pk>/delete',views.deleteDepartment,name="deletedepartment"),
    path('job-master/department-master/<str:pk>/edit',views.editDepartment,name="editdepartment"),
    path('job-master/designation-master/',views.DesignationMaster,name='designation-master'),
    path('job-master/designation-master/<str:pk>/delete',views.deleteDesignation,name="deletedesignation"),
    path('job-master/designation-master/<str:pk>/edit',views.editDesignation,name="editdesignation"),
    path('employees_profile/<str:pk>/delete',views.deleteEmployee,name='deleteemployee'),
    path('employees/',views.UserView,name='users'),
    path('employees/<int:pk>/edit',views.editUserView,name='edituser'),
    path('employees/<int:pk>/delete',views.deleteUser,name='deleteuser'),
    path('employees_profiles/<str:pk>/profile',views.employeeProfileView, name='employee_profile'),
    path('employees_profiles/<str:pk1>/profile/document/<str:pk2>/delete',views.deleteDocument, name='delete_document'),
    path('leave/leave-master/',views.LeaveMasterView,name='leave-master'),
    path('laeve/leave-master/<str:pk>/delete',views.deleteLeave,name="deleteleave"),
    path('leave/leave-master/<str:pk>/edit',views.editLeave,name="editleave"),
    path('leave/leave-applications/',views.LeaveApplicationView,name="leave-applications"),
    path('leave/leave-applications/approve/<str:pk>/', views.approve_leave, name='approve_leave'),
    path('leave/leave-applications/reject/<str:pk>/', views.reject_leave, name='reject_leave'),
    path('leave/leave-applications/delete/<str:pk>/', views.delete_leave, name='delete_leave'),
    path('master/holiday-master/',views.HolidayMaterView,name="holiday-master"),
    path('master/holiday-master/<str:pk>/delete',views.deleteHoliday,name="deleteholiday"),
    path('master/holiday-master/<str:pk>/edit',views.editHoliday,name="editholiday"),
   # api urls
    path('api/',include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)
