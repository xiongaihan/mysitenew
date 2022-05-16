import datetime
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import CommentForm


# Create your views here.

def updateComment(request):
    '''referer = request.META.get("HTTP_REFERER", reverse('home'))

    if not request.user.is_authenticated:
        return render(request, "error.html", {"message": "用户未登录"})

    text = request.POST.get('text', '').strip()

    if text == '':
        return render(request, "error.html", {"message": "评论不能为空"})

    try:
        # 获取对象
        content_type = request.POST.get('content_type', '')
        object_id = request.POST.get('object_id', '')
        model_class = ContentType.objects.get(model=content_type).model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except:
        # 防止博客被删除
        return render(request, "error.html", {"message": "评论对象不存在"})

    comment = Comment()
    comment.user = request.user
    comment.text = text
    comment.content_object = model_obj
    comment.save()
    return redirect(referer)'''

    referer = request.META.get("HTTP_REFERER", reverse('home'))

    comment_form = CommentForm(request.POST, user=request.user)
    data = {}
    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            print('parent.root',parent.root)
            if not parent.root is None:
                comment.root = parent.root
            else:
                comment.root = parent
            comment.parent = parent
            comment.reply_to = parent.user

        comment.save()
        # return redirect(referer)
        data['static'] = "SUCCES"
        data['username'] = comment.user.username
        data['comment_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data['text'] = comment.text
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        if not parent is None:
            data['reply_to'] = comment.reply_to.username
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''




    else:
        data['static'] = "ERROR"
        data['message'] = list(comment_form.errors.values())[0][0]
        # return render(request, "error.html", {"message": "对象不存在或者未登录","redirect_to":referer})

    return JsonResponse(data)
