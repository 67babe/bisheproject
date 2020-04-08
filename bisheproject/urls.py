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
    url(r'^index/', views.index),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^logout/', views.logout),
    url(r'^captcha', include('captcha.urls')), # 增加这一行
    url(r'^dynamic/', views.dynamic),
    url(r'^show_upload/', views.show_upload),#显示上传图片页面
    url(r'^upload_handle/', views.upload_handle),#上传图片处理
    url(r'^show_upload_dynamic', views.show_upload_dynamic),#上传图片处理
    url(r'^upload_dynamic_handle', views.upload_dynamic_handle),#上传图片处理




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#指定和映射静态文件的路径
