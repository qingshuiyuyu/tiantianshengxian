#coding:utf-8
from django.shortcuts import render,redirect
from models import *
from hashlib import sha1
from django.http import JsonResponse,HttpResponseRedirect
from django.core.paginator import Paginator,Page

# Create your views here.

def index(request):
    return render(request,'userhandle/index.html')

def login(request):
    context={'title':'登陆'}
    return render(request,'userhandle/login.html',context)

def register(request):
    context = {'title': '注册'}
    return render(request, 'userhandle/register.html',context)

def register_handle(request):
    #获取form表单用户所填写的数据
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    if upwd != upwd2:
        return redirect('/user/register/')

    #对密码进行加密sha1和MD5
    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()

    #创建对象
    user = UserInfo()
    user.user_name = uname
    user.password = upwd3
    user.user_email = uemail
    user.save()
    # 注册成功，转到登录页面
    return redirect('/user/login/')

def register_exist(request):
    uname=request.GET.get('uname')
    count=UserInfo.objects.filter(user_name=uname).count()
    return JsonResponse({'count':count})




def info(request):
    context = {'title': '用户信息'}
    return render(request, 'userhandle/user_center_info.html',context)
def site(request):
    return render(request, 'userhandle/user_center_site.html')
def order(request):
    return render(request, 'userhandle/user_center_order.html')