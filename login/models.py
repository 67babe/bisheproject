from django.db import models

# Create your models here.
# login/models.py

from django.db import models
from django.urls import reverse

class User(models.Model):
    gender = (
        ('男', '男'),
        ('女', '女'),
    )
    # user_id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    user_imag=models.ImageField(verbose_name='用户头像', upload_to='user_img/', default="user_img/默认头像.jpg",null=True, blank=True)
    profile=models.CharField(max_length=1000,null=True, blank=True,default="这个铲屎官很神秘，什么也没留下...")
    sex= models.CharField(max_length=32,choices=gender,default='男')


    def __str__(self):
        return self.name

    def get_following(self):
        '''
        following  关注的人
        :return:
        '''
        user_list = []
        for follower_user in self.follower.all():
            user_list.append(follower_user.following)
        return user_list

    def get_follower(self):
        '''
        follower 关注我的人
        :return:
        '''
        user_list = []
        for following_user in self.following.all():
            user_list.append(following_user.follower)
        return user_list





class FriendShip(models.Model):
    following = models.ForeignKey(User,related_name='following',on_delete=models.CASCADE)#关注
    follower = models.ForeignKey(User,related_name='follower',on_delete=models.CASCADE)#粉丝

class Dynamic(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    dynamic_id = models.AutoField(primary_key=True)
    dyn_text = models.CharField(max_length=1000)
    dyn_title = models.CharField(max_length=50)
    dyn_like = models.IntegerField(blank=False, null=False,default=0)
    dyn_time = models.DateTimeField(blank=True, null=True,auto_now_add=True)
    dyn_imag = models.ImageField(verbose_name='动态图片', upload_to='dynamic_img/', default="dynamic_img/默认动态.jpg",null=True, blank=True)

    def __str__(self):
        return self.dyn_title

    def delete_Dynamic(self):
        dynamic=Dynamic.objects.filter(dynamic_id=self.dynamic_id)
        if dynamic:
            dynamic.delete()#删除动态
            print("删除成功")
        else:
            print("找不到，没有删除成功")

    def get_absolute_url(self):
        return reverse('dynamic_detail', args=[self.dynamic_id])

class Pet(models.Model):

    gender = (
        ('男孩','男孩'),
        ('女孩','女孩'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet_id = models.AutoField(primary_key=True)
    pet_name = models.CharField(max_length=30)
    pet_age = models.IntegerField(blank=False, null=False,default=0)
    pet_sex = models.CharField(max_length=32,choices=gender,default='男孩')
    pet_imag = models.ImageField(verbose_name='宠物图片', upload_to='pet_img/',  default="pet_img/默认宠物.jpg",null=True, blank=True)

    def __str__(self):
        return self.pet_name


class Discuss(models.Model):
    dynamic = models.ForeignKey(Dynamic, on_delete=models.CASCADE,related_name='discuss')
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1,related_name='discuss')
    discuss_id = models.AutoField(primary_key=True)
    dis_text= models.CharField(max_length=1000,default=' ')
    dis_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.dis_text


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id=models.AutoField(primary_key=True)
    que_text = models.CharField(max_length=1000)
    que_title = models.CharField(max_length=50)
    que_like = models.IntegerField(blank=False, null=False,default=0)
    que_time = models.DateTimeField(blank=True, null=True)
    que_imag = models.ImageField(verbose_name='问题图片', upload_to='question_img/', null=True, blank=True)

    def __str__(self):
        return self.question_id

class PicTest(models.Model):
    goods_pic=models.ImageField(upload_to='booktest')

class Cat(models.Model):
    cat_imag = models.CharField(max_length=1000, default='');
    cat_name=models.CharField(max_length=50);
    cat_hometown = models.CharField(max_length=100);
    cat_weight = models.CharField(max_length=50);
    cat_life=models.CharField(max_length=50);
    cat_price=models.CharField(max_length=50);
