#coding:utf-8
from django.db import models

#订单信息
class OrderInfo(models.Model):
    oid = models.CharField(max_length=20,primary_key=True)#订单编号
    user = models.ForeignKey('userhandle.UserInfo')#用户名
    odate = models.DateTimeField(auto_now_add=True)#日期
    oIsPay = models.BooleanField(default=False)#是否支付
    ototal = models.DecimalField(max_digits=6, decimal_places=2)#总价
    oaddress = models.CharField(max_length=120)#订单地址

#订单详情
class OrderDetailInfo(models.Model):
    goods = models.ForeignKey('df_goods.GoodsInfo')#goods信息
    order = models.ForeignKey('OrderInfo')#订单信息
    price = models.DecimalField(max_digits=5,decimal_places=2)#订单物品单价
    count = models.IntegerField()#物品数量
