from django import forms
from django.contrib.auth.models import User


class ChangeNicknameForm(forms.Form):
    nickname_new = forms.CharField(label='新的昵称',
                                   max_length=20, widget=forms.TextInput
        (attrs={'class': 'form-control', 'placeholder': '请输入新的昵称'}))

    # 类的初始化方法
    def __init__(self, *args, **kwargs):
        print("初始化")
        self.user = None
        # 判断user是否在参数里面
        if 'user' in kwargs:
            # 在的话，剔除这个参数，以免父类初始化的时候报错
            self.user = kwargs.pop('user')
            print("用户：", self.user)
        super(ChangeNicknameForm, self).__init__(*args, **kwargs)

    def clean(self):

        if self.user:
            if self.user.is_authenticated:
                self.cleaned_data['user'] = self.user
            else:
                # print("用户未登录")
                raise forms.ValidationError('用户未登录')
        else:
            raise forms.ValidationError('用户未登录')
        return self.cleaned_data

    def clean_nickname_new(self):
        nickname_new = self.cleaned_data.get('nickname_new', '').strip()
        if nickname_new == '':
            raise forms.ValidationError('新昵称不能为空')
        return nickname_new


class BindEmailForm(forms.Form):
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput
    (attrs={'class': 'form-control', 'placeholder': '请输入正确的邮箱'}))
    verfication = forms.CharField(label='验证码', required=False, widget=forms.TextInput
    (attrs={'class': 'form-control', 'placeholder': '请输入验证码'}))

    # 类的初始化方法
    def __init__(self, *args, **kwargs):
        print("初始化")
        self.request = None
        # 判断user是否在参数里面
        if 'request' in kwargs:
            # 在的话，剔除这个参数，以免父类初始化的时候报错
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean(self):

        if self.request:
            if self.request.user.is_authenticated:
                self.cleaned_data['user'] = self.request.user
            else:
                # print("用户未登录")
                raise forms.ValidationError('用户未登录')
        else:
            raise forms.ValidationError('用户未登录')

        if self.request.user.email != '':
            raise forms.ValidationError("你已经绑定过邮箱了")

        # 判断验证码
        code = self.request.session.get('bind_email_code', '')
        verfication = self.cleaned_data.get('verfication', '')

        if not (code != '' and verfication == code):
            raise forms.ValidationError('验证码不正确')

        email = self.request.session.get('email', '')
        emailBind = self.cleaned_data.get('email', '')
        print(email, emailBind)

        if not (emailBind != '' and email == emailBind):
            raise forms.ValidationError('邮箱不正确')

        return self.cleaned_data


class ChangePasswordForm(forms.Form):
    ord_password = forms.CharField(label="旧密码",
                                   widget=forms.PasswordInput(attrs={"class": "form-control", 'placeholder': "请输入旧密码"}))
    new_password = forms.CharField(label="新密码",
                                   widget=forms.PasswordInput(attrs={"class": "form-control", 'placeholder': "请输入新密码"}))
    again_password = forms.CharField(label="确认密码",
                                     widget=forms.PasswordInput(
                                         attrs={"class": "form-control", 'placeholder': "确认新密码"}))

    # 类的初始化方法
    def __init__(self, *args, **kwargs):
        print("初始化")
        self.user = None
        # 判断user是否在参数里面
        if 'user' in kwargs:
            # 在的话，剔除这个参数，以免父类初始化的时候报错
            self.user = kwargs.pop('user')
            print("用户：", self.user)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        new_password = self.cleaned_data.get('new_password', '')
        again_password = self.cleaned_data.get('again_password', '')

        if new_password != again_password or new_password == '':
            raise forms.ValidationError("二次密码不一致")
        return self.cleaned_data

    # 验证原密码是否正确
    def clean_ord_password(self):
        ord_password = self.cleaned_data.get('ord_password', '')
        if not self.user.check_password(ord_password):
            raise forms.ValidationError('旧密码错误')
        return ord_password


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput
    (attrs={'class': 'form-control', 'placeholder': '请输入正确的邮箱'}))

    verfication = forms.CharField(label='验证码', required=False, widget=forms.TextInput
    (attrs={'class': 'form-control', 'placeholder': '请输入验证码'}))

    new_password = forms.CharField(label="新密码",
                                   widget=forms.PasswordInput(attrs={"class": "form-control", 'placeholder': "请输入新密码"}))
    again_password = forms.CharField(label="确认密码",
                                     widget=forms.PasswordInput(
                                         attrs={"class": "form-control", 'placeholder': "确认新密码"}))

    # 类的初始化方法
    def __init__(self, *args, **kwargs):
        print("初始化")
        self.request = None
        # 判断user是否在参数里面
        if 'request' in kwargs:
            # 在的话，剔除这个参数，以免父类初始化的时候报错
            self.request = kwargs.pop('request')
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        new_password = self.cleaned_data.get('new_password', '')
        again_password = self.cleaned_data.get('again_password', '')

        if new_password != again_password or new_password == '':
            raise forms.ValidationError("二次密码不一致")
            # 判断验证码
        code = self.request.session.get('forgot_code', '')
        verfication = self.cleaned_data.get('verfication', '')

        if not (code != '' and verfication == code):
            raise forms.ValidationError('验证码不正确')

        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱不存在')

        return email

