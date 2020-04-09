from django.db import models

# Create your models here.
# login/models.py

from django.db import models

class User(models.Model):
    gender = (
        ('男', '男'),
        ('女', '女'),
    )
    # user_id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    user_imag=models.ImageField(verbose_name='用户头像', upload_to='user_img/', null=True, blank=True)
    profile=models.CharField(max_length=1000,null=True, blank=True)
    sex= models.CharField(max_length=32,choices=gender,default='男')
    # c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    # class Meta:#元数据里定义用户按创建时间的反序排列，也就是最近的最先显示；
    #     ordering = ['c_time']
    #     verbose_name = '用户'
    #     verbose_name_plural = '用户'

class Dynamic(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    dynamic_id = models.AutoField(primary_key=True)
    dyn_text = models.CharField(max_length=1000)
    dyn_title = models.CharField(max_length=50)
    dyn_like = models.IntegerField(blank=False, null=False,default=0)
    dyn_time = models.DateTimeField(blank=True, null=True,auto_now_add=True)
    dyn_imag = models.ImageField(verbose_name='动态图片', upload_to='dynamic_img/', null=True, blank=True)

    def __str__(self):
        return self.dyn_text


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
    pet_imag = models.ImageField(verbose_name='宠物图片', upload_to='pet_img/', null=True, blank=True)

    def __str__(self):
        return self.pet_name


class Discuss(models.Model):
    dynamic = models.ForeignKey(Dynamic, on_delete=models.CASCADE)
    discuss_id = models.AutoField(primary_key=True)
    dis_text= models.CharField(max_length=1000,default=' ')
    dis_like = models.IntegerField(blank=False, null=False,default=0)
    dis_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.discuss_id


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
