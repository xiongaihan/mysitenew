from django.urls import path
from . import views

urlpatterns = [
    path('updateComment', views.updateComment, name="updateComment"),
]