from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentForm

register = template.Library()


@register.simple_tag
def get_comments_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    counts = Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()
    return counts


@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    # 初始化参数
    data = {}
    # 得到blog字符串
    data['content_type'] = content_type.model
    # 得到pk值
    data['object_id'] = obj.pk
    data['reply_comment_id'] = 0
    comment_form = CommentForm(initial=data)
    return comment_form

@register.simple_tag
def get_comments_list(obj):
    # 获取blog的contenttype对象
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None)
    return comments
