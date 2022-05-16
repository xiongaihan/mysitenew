from .models import LikeCount, LikeRecord
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType

def successResponse(like_num):
    data={}
    data['status']="SUCCESS"
    data['like_num']=like_num
    return JsonResponse(data)

def errorResponse(code,message):
    data={}
    data['status']="ERROR"
    data['code']=code
    data['message']=message

    return JsonResponse(data)

def like_change(request):
    user = request.user
    if not user.is_authenticated:
        return errorResponse(400,"未登录")
    # 获取提交的数据
    content_type = request.GET.get('content_type')

    object_id = int(request.GET.get('object_id'))
    try:
        content_type = ContentType.objects.get(model=content_type)
        # 获取整个model对象，相当于获取blog
        model_class=content_type.model_class()
        model_obj=model_class.objects.get(pk=object_id)
    except:
        errorResponse(405,"对象不存在")

    is_like = request.GET.get('is_like')

    # 处理数据
    if is_like == 'true':
        # 要点赞
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id,
                                                                user=user)
        if created:
            # 未点赞，进行点赞
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.liked_num += 1
            like_count.save()
            return successResponse(like_count.liked_num)
        else:
            # 已点赞过，不能重复点赞
            return errorResponse(402,'你已经点赞过')
    else:
        # 取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id,
                                     user=user).exists():
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id,
                                                 user=user)
            like_record.delete()

            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            # 如果点赞记录存在
            if not created:
                like_count.liked_num -= 1
                like_count.save()
                return successResponse(like_count.liked_num)
            else:
                return errorResponse(404,'数据错误')


        else:
            # 没有点赞过，不能取消
            return errorResponse(403,'你没有点赞过')
