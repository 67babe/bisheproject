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


class ProfileForm(forms.Form):
    gender = (
        ('男', '男'),
        ('女', '女'),
    )
    username = forms.CharField(label='昵称', max_length=50, required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile = forms.CharField(label='个人简介', max_length=1000, empty_value='这个铲屎官很神秘，没有留下仍和介绍...',required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label="性别",choices=gender,required=True)
    # user_imag = forms.ImageField(verbose_name='用户头像', upload_to='user_img/', required=False,null=True, blank=True) 单独做吧



# class DynamicForm(forms.Form):
#     title = forms.CharField(label="标题", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     text = forms.CharField(label="内容", max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))
#