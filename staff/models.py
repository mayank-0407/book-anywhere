from django.db import models
from django.contrib.auth.models import User

class Plan(models.Model):

    name=models.CharField(max_length=30)
    description=models.CharField(max_length=203,null=True)
    price=models.FloatField(null=True)

    def __str__(self):
        return self.name
