from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nickname = models.CharField(max_length=30)

    def __str__(self):
        return self.nickname + self.user.username


# 当这个方法绑定到类的时候，这个selfs参数代表对象本身，实际调用的时候，不能多传参数
def get_nickname(selfs):
    # 判断
    if Profile.objects.filter(user=selfs).exists():
        profile = Profile.objects.get(user=selfs)
        return profile.nickname
    else:
        return ''

def has_nickname(self):
    return Profile.objects.filter(user=self).exists()

def get_nickname_or_username(self):
    # 判断
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return self.username


User.get_nickname = get_nickname
User.has_nickname = has_nickname
User.get_nickname_or_username = get_nickname_or_username
