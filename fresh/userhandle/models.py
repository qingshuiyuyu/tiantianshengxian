#coding:utf-8
from django.db import models

# Create your models here.

class UserInfo(models.Model):
    user_name = models.CharField(max_length=20)
    password = models.CharField(max_length=40)
    user_email = models.CharField(max_length=30)
    user_phone = models.CharField(max_length=11,default='')
    user_adress = models.CharField(max_length=100,default='')
    post_code = models.CharField(max_length=6,default='')
    recipient = models.CharField(max_length=30,default='')



