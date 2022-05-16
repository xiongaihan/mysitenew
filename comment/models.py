from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


# Create your models here.
class Comment(models.Model):
    # 评论时间
    comment_time = models.DateTimeField(auto_now_add=True)
    # 评论内容，不限制数量
    text = models.TextField()
    # 用户
    user = models.ForeignKey(User, related_name='comment_user', on_delete=models.DO_NOTHING)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    parent = models.ForeignKey('self', related_name='comment_parent', null=True, on_delete=models.DO_NOTHING)
    root = models.ForeignKey('self',related_name='comment_root',null=True, on_delete=models.DO_NOTHING)
    reply_to = models.ForeignKey(User, null=True, related_name='reply_user', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.text

    # 设置返回数据顺序，和admin里面设置的顺序没有关系
    class Meta:
        ordering = ['-comment_time']
