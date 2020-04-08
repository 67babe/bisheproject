# from django import forms
#
#
# class UserForm(forms.Form):
#     # username = forms.CharField(label="用户名", max_length=128)
#     # password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput)

from django import forms
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    #form-control是模板里的
    # captcha = CaptchaField(label='验证码')
    #像写普通的form字段一样添加一个captcha字段就可以了！

class RegisterForm(forms.Form):

    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # captcha = CaptchaField(label='验证码')


# class DynamicForm(forms.Form):
#     title = forms.CharField(label="标题", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     text = forms.CharField(label="内容", max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))
#