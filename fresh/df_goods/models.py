#coding:utf-8
from django.db import models
from tinymce.models import HTMLField


# Create your models here.
class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.ttitle.encode('utf-8')

class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20)
    gpic = models.ImageField(upload_to='goods')
    gprice = models.DecimalField(max_digits=5,decimal_places=2)#最高5位数，小数点后保留两位
    isDelete = models.BooleanField(default=False)
    gunit = models.CharField(max_length=20,default='500g')#没份分量
    gclick = models.IntegerField()#点击量
    gjianjie = models.CharField(max_length=200)
    gkuncun = models.IntegerField()#库存,拼错了
    gcontent = HTMLField()#商品详情
    gtype = models.ForeignKey(TypeInfo)

    def __str__(self):
        return self.gtitle.encode('utf-8')

