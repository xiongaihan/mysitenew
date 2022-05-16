from django.shortcuts import render, redirect
from readApp.utils import get_seven_days_read_data, get_today_hot_data, get_yestoday_hot_data, get_seven_hot_data
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import  login,logout
from django.urls import reverse
from django.http import JsonResponse
from .forms import LoginForm, RegisterForm
from blog.models import Blog
from django.contrib import auth
from django.contrib.auth.models import User
from blog.util import get_seven_hot_blogs


def home(request):
    ct = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(ct)
    today_hot_data = get_today_hot_data(ct)
    yestoday_hot_data = get_yestoday_hot_data(ct)
    seven_hot_data = get_seven_hot_blogs()
    context = {}

    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = today_hot_data
    context['yestoday_hot_data'] = yestoday_hot_data
    context['seven_hot_data'] = seven_hot_data
    # print(seven_hot_data)
    return render(request, 'home.html', context)


def userLogin(request):
    # 获取post请求的数据
    # username = request.POST.get("userName", "")
    # password = request.POST.get("password", "")
    #
    # # 账号验证，如果存在的，并且密码正确的话，返回一个账号对象
    # user = authenticate(request, username=username, password=password)
    # # 获取到提交登录页面的地址，或者reverse反向获取到home链接
    # referer = request.META.get("HTTP_REFERER", reverse('home'))
    # print(referer)
    # if user is not None:
    #     # 账号登录
    #     login(request, user)
    #     # 重定向到其他页面
    #     return redirect(referer)
    # else:
    #     # 返回账号错误的页面
    #     return render(request, "error.html", {"message": "用户名或者密码错误"})
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 获取返回的user对象
            user = login_form.cleaned_data['user']
            login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        # 验证不成功才会重新创建这个form对象
        login_form = LoginForm()

    context = {}
    context['loginform'] = login_form
    # print("get请求", request.GET.get('from'))
    return render(request, 'login.html', context)

def login_for_medal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        # 获取返回的user对象
        user = login_form.cleaned_data['user']
        # 登录
        login(request, user)

        data['status']='SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)



# 注册
def rgister(request):
    if request.method == "POST":
        rgister_form = RegisterForm(request.POST)
        if rgister_form.is_valid():
            # 获取返回的user对象
            username = rgister_form.cleaned_data['username']
            email = rgister_form.cleaned_data['email']
            password = rgister_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username=username, password=password)
            user.email = email
            user.save()
            # 账号验证
            user = auth.authenticate(username=username, password=password)
            # 登录用户
            login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        # 验证不成功才会重新创建这个form对象
        rgister_form = RegisterForm()

    context = {}
    context['rgisterform'] = rgister_form
    # print("get请求", request.GET.get('from'))
    return render(request, 'rgister.html', context)

def login_out(request):
    logout(request)
    return redirect(request.GET.get('from', reverse('home')))
