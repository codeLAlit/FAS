from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class Employee(models.Model):
    emp_name=models.CharField(max_length=100, default="")
    emp_code=models.CharField(max_length=8, default="", unique=True)
    emp_photo=models.BooleanField(default=False)
    emp_encoding=models.BooleanField(default=False)
    
    def __str__ (self):
        return self.emp_code

class Record(models.Model):
    emp_name=models.CharField(max_length=100, default="")
    emp_code=models.CharField(max_length=8, default="")
    attendance_confi=models.FloatField()
    attendance_date=models.DateField()
    attendance_time=models.TimeField()
    remark=models.CharField(max_length=100, default="None")
    def __str__ (self):
        return self.emp_code