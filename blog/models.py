from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from readApp.models import ReadNumExpend, ReadDateNum


# 博客类型
class BlogType(models.Model):
    # 博客分类
    type_name = models.CharField(max_length=50)

    def get_type_name(self):
        return self.type_name

    def __str__(self):
        return self.type_name


# 博客模型
class Blog(models.Model, ReadNumExpend):
    # 博客标题
    title = models.CharField(max_length=50)
    # 博客类型，使用外键博客类型
    blog_type = models.ManyToManyField(BlogType)
    # 博客内容
    content = RichTextUploadingField()
    # 博客作者
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # 博客创建的时间
    created_time = models.DateTimeField(auto_now_add=True)
    # 博客更新的时间
    last_updated_time = models.DateTimeField(auto_now=True)
    # 反向关系，获取到所有此博客对象的ReadDateNum对象
    read_details = GenericRelation(ReadDateNum)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_time']
