from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

# login/views.py

# 顺序：设计数据库模型-数据库迁移-admin中注册模型-设计路由-构建初步视图函数-创建html-前端页面设计-补充视图函数
from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from django.conf import settings
from .models import User
from .models import Dynamic
from .models import Pet
from .models import Discuss
from .models import Question
from .models import Discuss
from .forms import UserForm
from .forms import ProfileForm
from .forms import RegisterForm
from .models import PicTest
from django.urls import reverse

import hashlib

def index(request):
    pass
    return render(request, 'login/index.html')


def login(request):

    if request.session.get('is_login',None):
        return redirect('/index')
     #不允许重复登录
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(name=username) #直接从数据库里搜
                if user.password == hash_code(password):  # 哈希值和数据库内的值进行比对
                    request.session['is_login'] = True       #往session字典内写入用户状态和数据：
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！？"
        return render(request, 'login/login.html', locals())
      # Python内置了一个locals()函数，它返回当前所有的本地变量字典
    login_form = UserForm()
    return render(request, 'login/login.html', locals())

#增加了message变量，用于保存提示信息。当有错误信息的时候，将错误信息打包成一个字典，然后作为第三个参数提供给render()方法。
# 这个数据字典 {"message": message} 在渲染模板的时候会传递到模板里供你调用。
# 用户通过login.html中的表单填写用户名和密码，并以POST的方式发送到服务器的/login/地址。
# 服务器通过login/views.py中的login()视图函数，接收并处理这一请求。

def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)# 先实例化一个RegisterForm的对象，然后使用is_valide()验证数据，再从cleaned_data中获取数据。
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']

            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 利用ORM的API，创建一个用户实例，然后保存到数据库内
                new_user = User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)  # 使用加密密码
                new_user.email = email
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())
# 从大体逻辑上，也是先实例化一个RegisterForm的对象，然后使用is_valide()验证数据，再从cleaned_data中获取数据。
#
# 重点在于注册逻辑，首先两次输入的密码必须相同，其次不能存在相同用户名和邮箱，最后如果条件都满足，利用ORM的API，创建一个用户实例，然后保存到数据库内。


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    # 方法是比较安全的一种做法，而且一次性将session中的所有内容全部清空，确保不留后患
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")


def hash_code(s, salt='67babe'):  # 加点盐嘻嘻
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def dynamic(request):
    data=Dynamic.objects.all() #.order_by('-pub_date')
    return render(request, 'dynamic/dynamic.html',context={'data':data})


def show_upload_dynamic(request):
    return render(request, 'dynamic/upload_dynamic.html')

def upload_dynamic_handle(request):
    #1。获取上传的图片的处理对象
    title = request.POST.get('title')
    pic = request.FILES['pic']
    text = request.POST.get('text')
    user = request.session.get('user_id')
    #2。创建一个文件
    save_path='%s/dynamic_img/%s'%(settings.MEDIA_ROOT,pic.name)
    with open(save_path,'wb')as f:
    #3。获取上传文件的内容并写到创建的文件中
        for content in pic.chunks():
            f.write(content)
    #4。在数据库中保存上传记录（路径）
    Dynamic.objects.create(dyn_imag ='dynamic_img/%s' % pic.name, dyn_text=text, dyn_title=title,user_id=user)
    # return render(request, 'dynamic/upload_pic.html')

    return HttpResponseRedirect('/dynamic/')

def home(request):
    # user = User.objects.get(name=username)  # 直接从数据库里搜
    userid = request.session.get('user_id')
    data = User.objects.get(id=userid)
    pets= Pet.objects.filter(user_id=userid)
    return render(request,'home/home.html',context={'data':data,'pets':pets})


def user_setting(request):
    userid = request.session.get('user_id')
    user = User.objects.get(id=userid)

    if request.method == "POST":
        form = ProfileForm(request.POST)

        if form.is_valid():
            user.name=form.cleaned_data['username']
            user.email=form.cleaned_data['email']
            user.sex=form.cleaned_data['sex']
            user.profile=form.cleaned_data['profile']
        user.save()
        return HttpResponseRedirect('/home/')

    else:
        default_data = {'username':user.name,'email':user.email,'sex':user.sex,'profile':user.profile}
        form = ProfileForm(default_data)
        return render(request, 'home/user_setting.html', {'form': form, 'user': user})
        # return HttpResponseRedirect(reverse('users:profile', args=[user.id]))
    # 在这个HttpResponseRedirect示例中，我们在的构造函数中使用reverse()
    # 函数。这个函数避免了我们在视图函数中的硬编码URL。它需要我们替换我们想要替换的视图的名字和该视图所对应的URL模式中需要给该视图提供的参数。在本例中，使用在教程第3部分中设置的URLconf，reverse()
    # 调用将返回一个这样的字符串：
    #
    # '/polls/3/results/'
    # 其中3是question.id的值。重定向的URL将调用
    # 'results'
    # 视图来显示最终的页面。



    user = User.objects.get(name=username)  # 直接从数据库里搜
    userid = get_object_or_404(User, pk=pk)
    data = User.objects.get(id=userid)
    pets= Pet.objects.filter(user_id=userid)
    return render(request,'home/home.html',context={'data':data,'pets':pets})







def show_upload(request):
    return render(request, 'dynamic/upload_pic.html')

def upload_handle(request):
    #1。获取上传的图片的处理对象
    pic = request.FILES['pic']

    #2。创建一个文件
    save_path='%s/booktest/%s'%(settings.MEDIA_ROOT,pic.name)
    with open(save_path,'wb')as f:
    #3。获取上传文件的内容并写到创建的文件中
        for content in pic.chunks():
            f.write(content)
    #4。在数据库中保存上传记录（路径）
    PicTest.objects.create(goods_pic='booktest/%s'% pic.name)


    # return render(request, 'dynamic/upload_pic.html')
    return HttpResponse('ok')