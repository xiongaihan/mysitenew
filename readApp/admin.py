from django.contrib import admin
from .models import ReadNum,ReadDateNum

# Register your models here.

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ("id","read_num","content_object")


@admin.register(ReadDateNum)
class ReadDateNumAdmin(admin.ModelAdmin):
    list_display = ("id","read_num","date","content_object","object_id")
    ordering = ("-date",)
