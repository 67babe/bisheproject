from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    # 发表评论
    path('post_comment/<int:dynamic_id>/', views.post_comment, name='post_comment'),
    path('delete_comment/<int:id>/', views.delete_comment, name='delete_comment'),
]
