import datetime
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from .models import Blog


def get_seven_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=6)

    blogs = cache.get('seven_hot_blogs')
    # print(blogs)
    # 如果没有缓存信息，则创建数据，并创建缓存
    if not blogs:
        # print("没有使用缓存")
        # 需要注意的是read_details__date这个数据来源于，blog对象的反向对象ReadDateNum的data属性，使用双下划线可以获取到属性值
        blogs = Blog.objects.filter(read_details__date__lte=today, read_details__date__gte=date) \
            .values('id', 'title') \
            .annotate(read_num_sum=Sum("read_details__read_num")) \
            .order_by('-read_num_sum')
        # 5s后失效
        cache.set('seven_hot_blogs', blogs, 5)
    else:
        pass
        # print("使用了缓存数据")

    return blogs[:3]
