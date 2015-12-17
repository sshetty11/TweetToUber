from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    user_name=models.CharField(max_length=100)
    phone_no=models.IntegerField(default=0)
    def __str__(self):
        return self.user_name
    
    
