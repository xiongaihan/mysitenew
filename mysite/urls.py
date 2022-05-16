"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home,userLogin,rgister,login_for_medal,login_out

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('userLogin/', userLogin, name='userLogin'),
    path('login_for_medal/', login_for_medal, name='login_for_medal'),
    path('login_out/', login_out, name='login_out'),
    path('rgister/', rgister, name='rgister'),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('likes/', include('likes.urls')),
    path('blog/', include('blog.urls')),
    path('user/', include('user.urls')),
    path('comment/', include('comment.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
