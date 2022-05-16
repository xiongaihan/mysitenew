from django.contrib import admin
from .models import Comment

# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id","text","comment_time","content_object")

    ordering = ("comment_time",)
