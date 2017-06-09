#coding:utf-8
from django.shortcuts import render
from models import *
from django.core.paginator import Paginator,Page
from django.http import HttpResponse
from df_cart.models import *

# Create your views here.
def index(request):
    type_list = TypeInfo.objects.all()
    list = []
    for type in type_list:
        list.append({
            'type':type,
            'click_list':type.goodsinfo_set.order_by('-gclick')[0:3],#此处为切片
            'new_list': type.goodsinfo_set.order_by('-id')[0:4],
        })
    context={'title':'天天生鲜',
             'list':list,
             'cart_count': cart_count(request),
             }
    return render(request, 'df_goods/index.html',context,)


def list(request,tid,pindex,sort):#(tid=typeinfo_id,pindx=页数,id=sort)
    # 查询指定分类tid的商品
    type = TypeInfo.objects.get(id=int(tid))
    goods_list = GoodsInfo.objects.filter(gtype_id=int(tid))
    news = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')[0:2]
    if sort == '1':
        goods_list = goods_list.order_by('-id')
    elif sort=='2':
        goods_list = goods_list.order_by('-gprice')
    elif sort == '3':
        goods_list = goods_list.order_by('-gclick')

    paginator = Paginator(goods_list, 10)
    pindex2 = int(pindex)
    if pindex2 <= 0:
        pindex2 = 1
    elif pindex2 > paginator.num_pages:
        pindex2 = paginator.num_pages
    page = paginator.page(pindex2)

    context = {'title': '列表页',
                'page':page,
                'paginator':paginator,
                'news':news,
                'tid':tid,
                'type':type,
                'sort':sort,
                'cart_count':cart_count(request),
               }
    return render(request,'df_goods/list.html',context)

def detail(request,pid):
    goods = GoodsInfo.objects.get(id=pid)
    goods.gclick = goods.gclick+1
    goods.save()
    new_list = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context={'title':'商品详情',
             'goods':goods,
             'news':new_list,
             'cart_count':cart_count(request),
             }
    response = render(request, 'df_goods/detail.html', context)


    goods_ids = request.COOKIES.get('goods_ids','')
    goods_id = ' %d '%goods.id
    if goods_ids != '':#判断cookie是否为空
        goods_ids1 = goods_ids.split(',')#对cookie（字符串）进行切片得到[]
        if goods_ids1.count(goods_id) >= 1:#如果浏览记录已存在
            goods_ids1.remove(goods_id)#将原浏览记录删除
        goods_ids1.insert(0, goods_id)#讲浏览记录插入到第一位
        if len(goods_ids1) >= 6:
            del goods_ids1[5]#删除第六个浏览记录
        goods_ids = ','.join(goods_ids1)#拼接为字符串
    else:
        goods_ids = goods_id#如果没有浏览记录则直接加
    response.set_cookie('goods_ids',goods_ids)#写入cookie

    return response



from haystack.views import SearchView
class MySearchView(SearchView):
    def extra_context(self):
        extra = super(MySearchView, self).extra_context()
        extra['title']=self.request.GET.get('q')
        extra['cart_count']=cart_count(self.request)
        return extra

def cart_count(request):
    if request.session.has_key('user_id'):
        return CartInfo.objects.filter(user_id=request.session['user_id']).count()
    else:
        return 0

