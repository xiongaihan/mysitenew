import string
import random
import time
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.mail import send_mail
# from django.contrib.auth import  login,logout
from .forms import ChangeNicknameForm, BindEmailForm, ChangePasswordForm, ForgotPasswordForm
from .models import Profile


def user_info(request):
    context = {}

    return render(request, 'user/user_info.html', context)


def change_nickname(request):
    redirectUrl = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            print("get_nickname", request.user.get_nickname())
            return redirect(redirectUrl)

    else:
        form = ChangeNicknameForm()

    context = {}
    context['form'] = form
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['redirectUrl'] = redirectUrl

    return render(request, 'form.html', context)


def bind_email(request):
    redirectUrl = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            # 绑定邮箱成功以后删除code
            del request.session['bind_email_code']
            return redirect(redirectUrl)



    else:
        form = BindEmailForm()

    context = {}
    context['form'] = form
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['redirectUrl'] = redirectUrl

    return render(request, 'user/bindEmail.html', context)


def send_verification_code(request):
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for', '')
    data = {}
    if email != '':
        # 生成验证码,随机生成四个字符串
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))

        # 时间限制
        now = int(time.time())
        send_time = request.session.get('send_time', 0)

        if (now - send_time) < 30:
            data['status'] = 'ERROR'
            return JsonResponse(data)
        # 发送邮件
        send_mail(
            '绑定邮箱',
            '验证码：%s' % code,
            '948709909@qq.com',
            [email],
            fail_silently=False,
        )
        request.session['send_time'] = now
        request.session[send_for] = code
        request.session['email'] = email
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'

    return JsonResponse(data)


def change_password(request):
    redirectUrl = reverse('home')
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            # logout(request)
            return redirect(redirectUrl)

    else:
        form = ChangePasswordForm()

    context = {}
    context['form'] = form
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['redirectUrl'] = redirectUrl

    return render(request, 'form.html', context)


def forgot_password(request):
    redirectUrl = reverse('home')
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            print('email',email)
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            # 绑定邮箱成功以后删除code
            del request.session['forgot_code']
            return redirect(redirectUrl)

    else:
        form = ForgotPasswordForm()

    context = {}
    context['form'] = form
    context['page_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '重置'
    context['redirectUrl'] = redirectUrl

    return render(request, 'user/forgot_password.html', context)
