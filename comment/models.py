from django.db import models
from login.models import Dynamic
from login.models import User
# Create your models here.
class Comment(models.Model):

    dynamic = models.ForeignKey(Dynamic, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='comments')
    com_text = models.TextField()
    com_time = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ('com_time',)

    def __str__(self):
        return self.com_text[:20]
