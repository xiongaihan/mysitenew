from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import LikeCount,LikeRecord

register = template.Library()


@register.simple_tag
def get_likes_count(obj):
    # 根据obj字符串对象获取content_type对象
    content_type = ContentType.objects.get_for_model(obj)
    like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=obj.pk)
    return like_count.liked_num


@register.simple_tag(takes_context=True)
def get_like_status(context, obj):
    # 根据对象获取content_type对象
    content_type = ContentType.objects.get_for_model(obj)
    user = context['user']

    if not user.is_authenticated:
        return ''
    if LikeRecord.objects.filter(content_type=content_type, object_id=obj.pk,user=user).exists():
        return 'active'
    else:
        return ''

@register.simple_tag
def get_like_type(obj):
    # 根据对象获取content_type对象
    content_type = ContentType.objects.get_for_model(obj)
    # 返回字符串
    return content_type.model

