from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget
from .models import Comment


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    # 配置富文本框的样式comment_ckeditor配置在settings里面
    text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'),
                           error_messages={'required': "评论内容不能为空"}
                           )
    # 设置回复id
    reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'reply_comment_id'}))

    # 类的初始化方法
    def __init__(self, *args, **kwargs):
        print("初始化")
        self.user = None
        # 判断user是否在参数里面
        if 'user' in kwargs:
            # 在的话，剔除这个参数，以免父类初始化的时候报错
            self.user = kwargs.pop('user')
            print("用户：", self.user)
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):

        if self.user:
            if self.user.is_authenticated:
                self.cleaned_data['user'] = self.user
            else:
                # print("用户未登录")
                raise forms.ValidationError('用户未登录')
        else:
            raise forms.ValidationError('用户未登录')
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']

        try:
            model_class = ContentType.objects.get(model=content_type).model_class()
            model_obj = model_class.objects.get(pk=object_id)
            self.cleaned_data['content_object'] = model_obj
        except ObjectDoesNotExist:
            raise forms.ValidationError('评论对象不存在')

        return self.cleaned_data

    def clean_reply_comment_id(self):
        reply_comment_id = self.cleaned_data['reply_comment_id']
        if reply_comment_id < 0:
            raise forms.ValidationError('回复出错')
        elif reply_comment_id == 0:
            self.cleaned_data['parent'] = None
        elif Comment.objects.filter(pk=reply_comment_id).exists():
            self.cleaned_data['parent'] = Comment.objects.get(pk=reply_comment_id)

        else:
            raise forms.ValidationError("回复出错")

        print(self.cleaned_data['parent'])

        return self.cleaned_data['parent']
