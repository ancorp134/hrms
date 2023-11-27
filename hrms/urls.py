from django.contrib import admin
from django.urls import path
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
    path('employees/',views.EmployeeView,name='employees'),
    path('employees/<str:pk>/delete',views.deleteEmployee,name='deleteemployee'),
    path('users/',views.UserView,name='users'),
    path('users/<int:pk>/edit',views.editUserView,name='edituser'),
    path('users/<int:pk>/delete',views.deleteUser,name='deleteuser'),
    path('employees/<str:pk>/profile',views.employeeProfileView, name='employee_profile'),
    path('employees/<str:pk1>/profile/document/<str:pk2>/delete',views.deleteDocument, name='delete_document'),
    path('update_bank_status/<str:bank_id>/', views.update_bank_status, name='update_bank_status'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)
