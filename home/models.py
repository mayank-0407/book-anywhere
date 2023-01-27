from django.db import models
from django.contrib.auth.models import User
from staff.models import Plan

# Create your models here.
class Company(models.Model):

    user=models.ForeignKey(User, on_delete= models.CASCADE ,null=True, blank=True)
    otp_code=models.CharField(max_length=100,null=True)
    plan= models.ForeignKey(Plan, null=True,blank=True,on_delete=models.SET_NULL)
    location=models.CharField(max_length=20,blank=True,null=True)

    def __str__(self):
        return self.user.username