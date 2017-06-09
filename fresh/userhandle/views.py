#coding=utf-8
from django.shortcuts import render,redirect
from models import *
from hashlib import sha1
from django.http import JsonResponse,HttpResponseRedirect
from . import user_decorator
from df_goods.models import *
from df_order.models import *
# from df_order.models import *
from django.core.paginator import Paginator,Page



# Create your views here.

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

def login(request):
    uname = request.COOKIES.get('uname', '')
    context={'title':'登录页面','error_name':0,'error_pwd':0, 'uname':uname}
    return render(request,'userhandle/login.html',context)

def login_handle(request):
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)

    users = UserInfo.objects.filter(user_name=uname)
    print uname

    if len(users) == 1:

        s1 = sha1()
        s1.update(upwd)
        upwd3 = s1.hexdigest()

        if upwd3 == users[0].password:
            url = request.COOKIES.get('red_url', '/')
            # red = HttpResponseRedirect(url)
            red = redirect(url)
            # 成功后删除转向地址，防止以后直接登录造成的转向
            red.set_cookie('red_url','', max_age=-1)

            if jizhu != 0 :
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)

            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'userhandle/login.html', context)
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'userhandle/login.html', context)


@user_decorator.login
def info(request):
    user_id = request.session['user_id']
    users = UserInfo.objects.filter(id = user_id)
    user_email = users[0].user_email
    user_name = users[0].user_name

    goods_list = []
    goods_ids = request.COOKIES.get('goods_ids','')
    if goods_ids != '':
        goods_ids1 = goods_ids.split(',')
        for goods_id in goods_ids1:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    context = {'title': '用户中心',
               'user_email': user_email,
               'user_name': user_name,
               'page_name':1,
               'goods_list':goods_list
            }

    return render(request, 'userhandle/user_center_info.html',context)

@user_decorator.login
def site(request):
    user_id = request.session['user_id']
    user = UserInfo.objects.get(id = user_id)
    if request.method == 'POST':
        post = request.POST
        user.post_code = post.get('upost')#邮编
        user.recipient = post.get('ushou')#收件人
        user.user_phone = post.get('uphone')#收件人电话
        user.user_adress = post.get('uaddress')
        user.save()
    context = {'title': '用户中心', 'user': user,'page_name':1,}
    return render(request, 'userhandle/user_center_site.html', context)

@user_decorator.login
def order(request,pindex):
    order_list =OrderInfo.objects.filter(user_id=request.session['user_id']).order_by('-oid')
    paginator = Paginator(order_list,2)
    if pindex =='':
        pindex='1'
    page=paginator.page(int(pindex))


    context = {'title': '用户中心',
               'page_name': 1,
               'paginator':paginator,
               'page':page,
               }
    return render(request, 'userhandle/user_center_order.html',context)

#退出登陆
def logout(request):
    request.session.flush()
    return redirect('/')