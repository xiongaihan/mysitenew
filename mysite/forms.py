from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    # 设置此字段为必填项
    username = forms.CharField(label="用户名或邮箱", required=True,
                               widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "请输入用户名或邮箱"}))
    password = forms.CharField(label="密码",
                               widget=forms.PasswordInput(attrs={"class": "form-control", 'placeholder': "请输入密码"}))

    # 验证
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        # 账号验证
        user = auth.authenticate(username=username, password=password)
        if user is None:
            if User.objects.filter(email=username).exists():
                username = User.objects.get(email=username).username
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    # 返回验证成功的用户
                    self.cleaned_data['user'] = user
                    # 这个方法必须有返回
                    return self.cleaned_data
            raise forms.ValidationError('用户名或密码不正确')
        else:
            # 返回验证成功的用户
            self.cleaned_data['user'] = user
            # 这个方法必须有返回
            return self.cleaned_data




class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", required=True,
                               max_length=30,
                               min_length=3,
                               widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "请输入3-30位用户名"}))
    email = forms.EmailField(label="邮箱",
                             widget=forms.EmailInput(attrs={"class": "form-control", 'placeholder': "请输入邮箱"})
                             )
    password = forms.CharField(label="密码",
                               min_length=6,
                               widget=forms.PasswordInput(attrs={"class": "form-control", 'placeholder': "请输入至少6位密码"}))

    password_again = forms.CharField(label="确认密码",
                                     widget=forms.PasswordInput(
                                         attrs={"class": "form-control", 'placeholder': "请再次输入密码"}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')

        return self.cleaned_data['username']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')

        return self.cleaned_data['email']

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('二次输入的密码不一致')

        return self.cleaned_data['password']
