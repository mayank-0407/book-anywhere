from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('temp/', views.temp,name="temp"),
    path('signout/', views.signout,name="signout"),
    path('signin/', views.signin,name="signin"),
    path('signin/forgot/pass', views.forgot_pass,name="forgot_pass"),
    path('signup/<str:plan_id>', views.signup,name="signup"),
    path('signup/verify/<str:code>',views.activate_by_email,name="activate_email"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('Profile/verify/<str:code>/',views.activate_forgot_by_email,name="activate_forgot_pass"),
    path('change/pass/',views.email_for_change_verified, name="email_for_change_verified"),
]