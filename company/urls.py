from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    
    path('', views.cdashboard,name="cdashboard"),
    path('temp/', views.temp,name="temp"),
    path('Profile/', views.view_profile,name="view_profile"),
    path('Profile/change/password', views.change_pass,name="change_pass"),
    path('Profile/verify/<str:code>',views.activate_forgot_by_email,name="activate_forgot_pass"),
    path('mEmployee/', views.mEmployee,name="mEmployee"),
    path('addEmployee/', views.addEmployee,name="addEmployee"),
    path('delEmployee/<int:id>/', views.delEmployee, name='delEmployee'),
    path('mdesk/', views.mdesk,name="mdesk"),
    path('addDesk/', views.addDesk,name="addDesk"),
    path('Desk_upload/', views.desk_upload,name="desk_upload"),
    path('employee_upload/', views.employee_upload,name="employee_upload"),
    path('edashboard/', views.edashboard,name="edashboard"),
    path('bookDesk/', views.bookDesk,name="bookDesk"),
    path('mdesk/submit/', views.editDesk, name='editDesk'),
    
    
]