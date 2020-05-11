from django.contrib import admin
from . import models
from comment.models import Comment
# Register your models here.

admin.site.register(models.User)
admin.site.register(models.PicTest)
admin.site.register(models.Discuss)
admin.site.register(models.Dynamic)
admin.site.register(models.Pet)
admin.site.register(models.Question)
admin.site.register(models.FriendShip)
admin.site.register(Comment)
admin.site.register(models.Cat)
#
# class MyAdminSite(admin.AdminSite):
#     site_header = '67的猫猫之家管理系统'  # 此处设置页面显示标题
#     site_title = '67的猫猫之家'  # 此处设置页面头部标题
#
#
# admin_site = MyAdminSite(name='management')