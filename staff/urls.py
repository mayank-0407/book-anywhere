from django.urls import path
from django.urls import include
from . import views

urlpatterns = [


    path('', views.staffdashboard,name="staffdashboard"),
    path('plan/view/', views.setplan,name="setplan"),
    path('plan/add/', views.addplan,name="addplan"),
    path('plan/del/<str:plan_id>', views.delplan,name="delplan"),
]