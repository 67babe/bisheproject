"""bisheproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from login import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^unlogin_index/', views.unlogin_index),
    url(r'^index/', views.index),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^logout/', views.logout),
    url(r'^captcha', include('captcha.urls')), # 增加这一行
    url(r'^dynamic/', views.dynamic),
    url(r'^cat/', views.cat),
    url(r'^search_cat/$', views.search_cat, name='search_cat'),
    path('dynamic_detail/<int:id>/', views.dynamic_detail,name='dynamic_detail'),#显示用户个人页面
    url(r'^my_dynamic/', views.my_dynamic),
    path('delete_dynamic/<int:id>/', views.delete_dynamic,name='delete_dynamic'),
    # url(r'^delete_dynamic/', views.delete_dynamic),
    # url(r'^show_upload/', views.show_upload),#显示上传图片页面
    # url(r'^upload_handle/', views.upload_handle),#上传图片处理
    # url(r'^show_upload_dynamic', views.show_upload_dynamic),#上传图片处理
    url(r'^upload_dynamic', views.upload_dynamic),#上传动态
    path('home/<int:userid>/', views.home, name='home'),#个人主页
    # path('pet_profile/<int:pet_id>/', views.pet_profile, name='pet_profile'),#
    url(r'^user_setting/', views.user_setting),#用户资料设置
    url(r'^pwd_change/', views.pwd_change),#修改密码
    url(r'^pet/', views.pet),#宠物页面
    url(r'^add_pet/', views.add_pet),#添加宠物
    path('delete_pet/<int:id>/', views.delete_pet, name='delete_pet'),
    # url(r'^delete_pet/$', views.delete_pet, name="delete_pet"),
    url(r'^my_following/', views.my_following),#我的关注
    url(r'^my_follower/', views.my_follower),#我的粉丝
    path('show_profile/<int:userid>/', views.show_profile,name='show_profile'),#显示用户个人页面
    url(r'^search_dynamic/$', views.search_dynamic, name='search_dynamic'),
    path('comment/', include('comment.urls', namespace='comment')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#指定和映射静态文件的路径
