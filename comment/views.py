from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from login.models import Dynamic
from login.models import User
from .forms import CommentForm
from .models import Comment

# 评论

def post_comment(request, dynamic_id):
    dynamic = get_object_or_404(Dynamic, dynamic_id=dynamic_id)
    userid = request.session.get('user_id')
    user = User.objects.get(id=userid)
    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.dynamic = dynamic
            new_comment.user = user
            new_comment.save()
            return redirect(dynamic)
        # redirect()：返回到一个适当的url中：即用户发送评论后，重新定向到文章详情页面。当其参数是一个Model对象时，会自动调用这个Model对象的get_absolute_url()
        # 方法。因此接下来马上修改dynamic的模型。
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 处理错误请求
    else:
        return HttpResponse("发表评论仅接受POST请求。")

def delete_comment(request,id):
    comment=Comment.objects.get(id=id)
    dynamic=Dynamic.objects.get(dynamic_id=comment.dynamic.dynamic_id)
    comment.delete()#删除
    return redirect(dynamic)