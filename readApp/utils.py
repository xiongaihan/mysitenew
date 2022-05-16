import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from .models import ReadNum, ReadDateNum


def read_num_once(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)

    if not request.COOKIES.get(key):
        # 总的计数
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

        # 日期的计数
        date = timezone.now().date()
        readDate, created = ReadDateNum.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readDate.read_num += 1
        readDate.save()

    return key


def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    read_nums = []
    dates = []
    for i in range(6, -1, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime("%m/%d"))
        # 此处只过滤content_type和date字段
        read_details = ReadDateNum.objects.filter(content_type=content_type, date=date)
        # 聚合函数，统计每个对象的read_num对象的和
        result = read_details.aggregate(read_num_sum=Sum("read_num"))
        # print(result['read_num_sum'])
        read_nums.append(result['read_num_sum'] or 0)

    return dates, read_nums


# 获取今日的热门博客数据
def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDateNum.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    # 只返回前3条数据
    return read_details[:3]


# 获取昨日的热门数据
def get_yestoday_hot_data(content_type):
    today = timezone.now().date()
    date = today - datetime.timedelta(days=1)
    read_details = ReadDateNum.objects.filter(content_type=content_type, date=date).order_by('-read_num')
    # 只返回前3条数据
    return read_details[:3]


# 获取前七日的数据
def get_seven_hot_data(content_type):
    today = timezone.now().date()
    date = today - datetime.timedelta(days=6)
    read_details = ReadDateNum.objects.filter(content_type=content_type, \
        date__lte=today, date__gte=date) \
        .values('content_type','object_id') \
        .annotate(read_num_sum=Sum("read_num"))\
        .order_by('-read_num_sum') \
        # 只返回前3条数据


    return read_details[:3]
