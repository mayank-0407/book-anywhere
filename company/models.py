from django.db import models
from django.contrib.auth.models import User
from home.models import Company
from datetime import datetime
# Create your models here.
class Employee(models.Model):

    user=models.ForeignKey(User, on_delete= models.CASCADE ,null=True, blank=True)
    otp_code=models.CharField(max_length=100,null=True)
    company=models.ForeignKey(Company, on_delete= models.SET_NULL ,null=True, blank=True)
    # employee_id=models.CharField(max_length=15, null=True, blank=True)
    def __str__(self):
        return self.user.username

class Desk(models.Model):
    
    company = models.ForeignKey(Company,on_delete=models.CASCADE, null=True, blank=True)
    zone=models.CharField(max_length=20,blank=True,null=True)
    monitorCount=models.IntegerField(null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL,null=True,blank=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    status=models.IntegerField(default=1)
    uniqueID=models.IntegerField(default=0)
    #  1   booked
    #  2   available
    #  3   repair    

    def __str__(self):
        return self.zone