from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

# login/views.py

# 顺序：设计数据库模型-数据库迁移-admin中注册模型-设计路由-构建初步视图函数-创建html-前端页面设计-补充视图函数
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.conf import settings
from .models import User
from .models import Dynamic
from .models import Pet
from .models import Discuss
from .models import Question
from .models import Discuss
from .models import FriendShip
from .forms import UserForm
from .forms import ProfileForm
from .forms import RegisterForm
from .forms import PwdForm
from .forms import PetForm
from .forms import DynamicForm
from comment.models import Comment
from .models import PicTest
from django.db.models import Q
from django.urls import reverse

import hashlib


def index(request):
    if request.session.get('is_login', None):
        userid = request.session.get('user_id')
        user_head = User.objects.get(id=userid)  # 专门做头像用
    return render(request, 'login/index.html',locals())

def unlogin_index(request):
    pass
    return render(request, 'login/unlogin_index.html',locals())

def login(request):
    pass
    return render(request, 'login.html',locals())

def login(request):
    if request.session.get('is_login', None):
        return redirect('/index')
    # 不允许重复登录
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(name=username)  # 直接从数据库里搜
                # if user.password == hash_code(password):  # 哈希值和数据库内的值进行比对
                if user.password == password:  # 哈希值和数据库内的值进行比对
                    request.session['is_login'] = True  # 往session字典内写入用户状态和数据：
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')

                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())
    # Python内置了一个locals()函数，它返回当前所有的本地变量字典
    login_form = UserForm()
    return render(request, 'login/login.html', locals())


# 增加了message变量，用于保存提示信息。当有错误信息的时候，将错误信息打包成一个字典，然后作为第三个参数提供给render()方法。
# 这个数据字典 {"message": message} 在渲染模板的时候会传递到模板里供你调用。
# 用户通过login.html中的表单填写用户名和密码，并以POST的方式发送到服务器的/login/地址。
# 服务器通过login/views.py中的login()视图函数，接收并处理这一请求。

def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)  # 先实例化一个RegisterForm的对象，然后使用is_valide()验证数据，再从cleaned_data中获取数据。
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
                new_user.password = password1  # 使用加密密码
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


def my_following(request):#我的关注
    userid = request.session.get('user_id')
    user = User.objects.get(id=userid)
    user_head=User.objects.get(id=userid)#专门做头像用
    data=user.get_following()
    return render(request, 'home/my_following.html', locals())


def my_follower(request):#我的粉丝
    userid = request.session.get('user_id')
    user = User.objects.get(id=userid)
    user_head = User.objects.get(id=userid)  # 专门做头像用
    data=user.get_follower()
    return render(request, 'home/my_follower.html', locals())


# def set_following(request):  # 添加关注
#     userid = request.session.get('user_id')
#     user = User.objects.get(id=userid)
#     user.set_following()
#     return  HttpResponse('关注成功')
#
#
# def delete_following(request):#取消关注
#     userid = request.session.get('user_id')
#     user = User.objects.get(id=userid)
#     user.delete_following()
#     return  HttpResponse('取消关注成功')



def hash_code(s, salt='67babe'):  # 加点盐嘻嘻
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

def search_dynamic(request):
    userid = request.session.get('user_id')
    user = User.objects.get(id=userid)
    user_head = User.objects.get(id=userid)  # 专门做头像用
    q = request.GET.get('q')
    print(q)
    error_msg = ''
    if not q:
        error_msg = '请输入关键词'
        return render(request, 'dynamic/dynamic.html',locals())

    dynamic_list = Dynamic.objects.filter(dyn_title__icontains=q)
    if dynamic_list:
        print('找到了')
    return render(request, 'dynamic/search_dynamic_result.html', locals())

def dynamic(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    userid = request.session.get('user_id')
    user = User.objects.get(id=userid)
    user_head = User.objects.get(id=userid)  # 专门做头像用
    data = Dynamic.objects.all() # .order_by('-pub_date')
    # comment=Comment.objects.filter(dynamic_id=)
    return render(request, 'dynamic/dynamic.html',locals())

def dynamic_detail(request,id):
    userid = request.session.get('user_id')
    user = User.objects.get(id=userid)
    user_head = User.objects.get(id=userid)  # 专门做头像用
    data= Dynamic.objects.get(dynamic_id=id)
    comments = Comment.objects.filter(dynamic_id=id)
    # 添加comments上下文
    context = {'dynamic': dynamic, 'comments': comments}

    return render(request, 'dynamic/dynamic_detail.html', locals())

def my_dynamic(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    userid = request.session.get('user_id')
    user = User.objects.get(id=userid)
    user_head = User.objects.get(id=userid)  # 专门做头像用
    data = Dynamic.objects.filter(user_id=userid) # .order_by('-pub_date')
    return render(request, 'dynamic/my_dynamic.html',locals())

def delete_dynamic(request,id):
    dynamic=Dynamic.objects.get(dynamic_id=id)
    if dynamic:
        dynamic.delete_Dynamic()#删除动态
        print("删除成功")
    return HttpResponseRedirect('/dynamic/')

# def show_upload_dynamic(request):
#     userid = request.session.get('user_id')
#     user = User.objects.get(id=userid)
#     user_head = User.objects.get(id=userid)  # 专门做头像用
#     return render(request, 'dynamic/upload_dynamic.html',locals())


def upload_dynamic(request):
    userid = request.session.get('user_id')
    user = User.objects.get(id=userid)
    user_head = User.objects.get(id=userid)  # 专门做头像用

    if request.method == "POST":
        form = DynamicForm (request.POST, request.FILES)
        if form.is_valid():
            if request.FILES.get('imag'):
                title = form.cleaned_data['title']
                text = form.cleaned_data['text']
                # imag = request.FILES['imag']
                imag = request.FILES.get('imag')
                new_dynamic = Dynamic.objects.create(user_id=userid)
                new_dynamic.dyn_title = title
                new_dynamic.dyn_text = text
                new_dynamic.dyn_imag = imag
                new_dynamic.save()
                return redirect('/dynamic/')  # 自动跳转到
            else:
                title = form.cleaned_data['title']
                text = form.cleaned_data['text']
                # imag = request.FILES['imag']
                # imag = request.FILES.get('imag')
                new_dynamic = Dynamic.objects.create(user_id=userid)
                new_dynamic.dyn_title=title
                new_dynamic.dyn_text = text
                # new_dynamic.dyn_imag = imag
                new_dynamic.save()
                return redirect('/dynamic/')  # 自动跳转到
    form = DynamicForm()
    return render(request, 'dynamic/upload_dynamic.html', locals())

    # # 1。获取上传的图片的处理对象
    # title = request.POST.get('title')
    # pic = request.FILES['pic']
    # text = request.POST.get('text')
    # user = request.session.get('user_id')
    # # 2。创建一个文件
    # save_path = '%s/dynamic_img/%s' % (settings.MEDIA_ROOT, pic.name)
    # with open(save_path, 'wb')as f:
    #     # 3。获取上传文件的内容并写到创建的文件中
    #     for content in pic.chunks():
    #         f.write(content)
    # # 4。在数据库中保存上传记录（路径）
    # Dynamic.objects.create(dyn_imag='dynamic_img/%s' % pic.name, dyn_text=text, dyn_title=title, user_id=user)
    # # return render(request, 'dynamic/upload_pic.html')
    #
    # return HttpResponseRedirect('/dynamic/')





def home(request,userid):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")

    # user = User.objects.get(name=username)  # 直接从数据库里搜
    # userid =
    userid=userid
    data = User.objects.get(id=userid)
    user_head = User.objects.get(id=userid)  # 专门做头像用
    pets = Pet.objects.filter(user_id=userid)
    dynamic=Dynamic.objects.filter(user_id=userid)
    dynamic2=dynamic.order_by('dynamic_id')[:3]
    pets2 = pets.order_by('pet_id')[:3]
    following_number =FriendShip.objects.filter(following=userid)
    follower_number = FriendShip.objects.filter(follower=userid)
    return render(request, 'home/home.html', locals())

def show_profile(request,userid):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    userid1 = request.session.get('user_id')# 专门做头像用
    user_head = User.objects.get(id=userid1)  # 专门做头像用
    userid=userid
    user_info = User.objects.get(id=userid)         # URL中指向的是哪个用户的profile页面
    userid2 = request.session.get('user_id')# 登录用户自己的用户信息，用于Follow
    self_user=User.objects.get(id=userid2)
    to_follow_user = User.objects.get(id=userid)    # 通过URL获取的对象信息，用于Follow
    data = User.objects.get(id=userid)
    pets = Pet.objects.filter(user_id=userid)
    pets2=pets.order_by('pet_id')[:2]
    dynamic = Dynamic.objects.filter(user_id=userid)
    dynamic2 = dynamic.order_by('dynamic_id')[:3]
    following_number = FriendShip.objects.filter(following=userid)
    follower_number = FriendShip.objects.filter(follower=userid)

    if not FriendShip.objects.filter(follower=self_user, following=to_follow_user): # 如果登录用户和对象用户没有关注
        show_button = "关注"
        if request.method == "POST":
            relationship = FriendShip()
            relationship.following = User.objects.get(id=to_follow_user.id)  # 要去关注谁
            relationship.follower = User.objects.get(id=self_user.id)  # 由谁来关注
            relationship.save()
            return redirect('show_profile', userid)
        else:
            return render(request, 'home/show_profile.html', locals())
    else:
        show_button = "取消关注"
        if request.method == "POST":
            relationship = FriendShip.objects.get(follower=self_user, following=to_follow_user)
            relationship.delete()
            return redirect('show_profile', userid)
        else:
            return render(request, 'home/show_profile.html', locals())
    return render(request, 'home/show_profile.html', locals())





def pet(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    userid = request.session.get('user_id')
    user_head = User.objects.get(id=userid)  # 专门做头像用
    pets = Pet.objects.filter(user_id=userid)
    return render(request, 'Pet/pet.html', locals())

# def pet_profile(request,pet_id):
#     userid = request.session.get('user_id')
#     pet_id = pet_id
#     pets=Pet.objects.get(pet_id=pet_id)
#     data = User.objects.get(id=userid)
#     user_head = User.objects.get(id=userid)  # 专门做头像用
#     return render(request, 'Pet/pet_profile.html', locals())

def add_pet(request):
    userid = request.session.get('user_id')
    user = User.objects.get(id=userid)
    user_head = User.objects.get(id=userid)  # 专门做头像用
    if request.method == "POST":
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            if  request.FILES.get('pet_img'):
                pet_name = form.cleaned_data['pet_name']
                pet_age = form.cleaned_data['pet_age']
                pet_sex = form.cleaned_data['pet_sex']
                pet_imag = request.FILES.get('pet_img')
                new_pet = Pet.objects.create(user_id=userid)
                new_pet.pet_name = pet_name
                new_pet.pet_age = pet_age
                new_pet.pet_sex = pet_sex
                new_pet.pet_imag = pet_imag
                new_pet.save()
                return redirect('/pet/')  # 自动跳转到
            else:
                pet_name = form.cleaned_data['pet_name']
                pet_age = form.cleaned_data['pet_age']
                pet_sex = form.cleaned_data['pet_sex']
                new_pet = Pet.objects.create(user_id=userid)
                new_pet.pet_name = pet_name
                new_pet.pet_age = pet_age
                new_pet.pet_sex = pet_sex
                new_pet.save()
                return redirect('/pet/')  # 自动跳转到
    form = PetForm()
    return render(request, 'pet/add_pet.html', locals())

def delete_pet(request,id):
    pet=Pet.objects.get(pet_id=id)
    pet.delete()
    print('调用删除啦')
    print(id)
    return redirect('/pet/')

def user_setting(request):
    userid = request.session.get('user_id')
    user = User.objects.get(id=userid)
    user_head = User.objects.get(id=userid)  # 专门做头像用
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        message = "请检查填写的内容！"
        if form.is_valid():
            if request.FILES.get('imag'):
                user.name = form.cleaned_data['username']
                user.email = form.cleaned_data['email']
                user.sex = form.cleaned_data['sex']
                user.profile = form.cleaned_data['profile']
                user.user_imag = request.FILES.get('imag')
                # if not user.user_imag:
                #     message = "请选择图片！"
                #     return render(request, 'home/user_setting.html', locals())
                user.save()

            else:
                user.name = form.cleaned_data['username']
                user.email = form.cleaned_data['email']
                user.sex = form.cleaned_data['sex']
                user.profile = form.cleaned_data['profile']
                user.user_imag=user_head.user_imag
                # if not user.user_imag:
                #     message = "请选择图片！"
                #     return render(request, 'home/user_setting.html', locals())
                user.save()
                print("没选")
        else:
            message = "请选择图片！"
            return render(request, 'home/user_setting.html', locals())
        return HttpResponseRedirect('/home/'+str(userid))

    else:
        default_data = {'username': user.name, 'email': user.email, 'sex': user.sex, 'profile': user.profile,'imag':user.user_imag}
        print("form无效")
        print(user.user_imag)
        form = ProfileForm(default_data)
        return render(request, 'home/user_setting.html', locals())
    data = User.objects.get(id=userid)
    pets = Pet.objects.filter(user_id=userid)
    return render(request, 'home/home.html', locals())


def pwd_change(request):
    userid = request.session.get('user_id')
    user = User.objects.get(id=userid)
    user_head = User.objects.get(id=userid)  # 专门做头像用
    if request.method == "POST":
        form = PwdForm(request.POST)
        message = "请检查填写的内容！"
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            new_password2 = form.cleaned_data['new_password2']

            if user.password != old_password:  # 哈希值和数据库内的值进行比对
                message = "密码错误！"
                return render(request, 'home/pwd_change.html', locals())
            else:
                if new_password != new_password2:  # 判断两次密码是否相同
                    message = "两次输入的密码不同！"
                    return render(request, 'home/pwd_change.html', locals())
                user.password = new_password
                user.save()
                return redirect('/home/'+str(userid))
    form = PwdForm()
    return render(request, 'home/pwd_change.html', locals())


