#coding:utf-8
from django.shortcuts import render,redirect
from django.http import HttpResponse
from df_cart.models import CartInfo
from df_goods.models import GoodsInfo
from models import *
from django.db import transaction#引入事务
from datetime import datetime#引入时间

# Create your views here.

@transaction.atomic
def order(request):
    post = request.POST
    address = post.get('address')
    cart_id = post.getlist('cart_id')
    sid = transaction.savepoint()

    try:
        #创建新订单对象
        order = OrderInfo()
        now = datetime.now()
        uid = request.session['user_id']
        order.oid = '%s%d'%(now.strftime('%Y%m%d%H%M%S'),uid)#订单id
        order.user_id = uid#用户id
        order.odate = now#订单时间
        order.oaddress = address#订单地址
        order.ototal = 0#订单总价
        order.save()#保存
        #计算总金额
        total = 0
        #判断购物车中数量是否足够库存
        for cid in cart_id:
            cart = CartInfo.objects.get(pk=cid)
            if cart.goods.gkuncun>=cart.count:
                #如果库存足够
                cart.goods.gkuncun -= cart.count
                cart.goods.save()
                cart.goods.save()
                #添加详单信息
                detail = OrderDetailInfo()
                detail.order = order
                detail.goods = cart.goods
                detail.price = cart.goods.gprice
                detail.count = cart.count
                detail.save()
                total += cart.goods.gprice * cart.count
                # 删除购物车数据
                cart.delete()
            else:
                #如果库存不够，则回滚
                #print ('库存不够')#测试用
                transaction.savepoint_rollback(sid)

        order.ototal=total
        order.save()
        transaction.savepoint_commit(sid)
        #print('ok')#测试用
        return redirect('/user/order')
    except:
        print('报错！')
        transaction.savepoint_rollback(sid)
        return redirect('/cart/')

def pay(request,oid):
    order = OrderInfo.objects.get(pk=oid)
    order.oIsPay = True
    order.save()
    return redirect('/user/order/')