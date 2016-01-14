from __future__ import unicode_literals
from django.db import models

# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=100)
    user_name=models.CharField(default="nothing",max_length=100)
    address=models.CharField(max_length=500,default="nothing")
    phone_no=models.IntegerField(default=0)
    access_token=models.CharField(default="nothing",max_length=500)
    def __str__(self):
        return self.user_name

class Request(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    request_id=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    
    
