#coding:utf-8

from django.db import models
from df_goods.models import *
from userhandle.models import *

# Create your models here.
class CartInfo(models.Model):
    goods = models.ForeignKey(GoodsInfo)
    count = models.IntegerField()
    user = models.ForeignKey(UserInfo)


