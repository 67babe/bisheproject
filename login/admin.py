from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.User)
admin.site.register(models.PicTest)
admin.site.register(models.Discuss)
admin.site.register(models.Dynamic)
admin.site.register(models.Pet)
admin.site.register(models.Question)
admin.site.register(models.FriendShip)