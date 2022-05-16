from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from .models import Blog, BlogType
from readApp.utils import read_num_once
from mysite.forms import LoginForm


def blog_list_common_date(request, blog_all_list):
    paginator = Paginator(blog_all_list, settings.PAGINATOR_NUBBER)
    # 获取url的页面请求的参数，如果有page就回去，没有就返回1
    page_num = request.GET.get('page', 1)
    # 这个可以返回一页，如果参数不是int或者数字，随便写的，也会返回第一页，或者最后一页
    page_of_blogs = paginator.get_page(page_num)
    # 获取当前的页码，不直接使用page_num的原因是，有可能用户输入的字符串
    current_page_nubmer = page_of_blogs.number
    page_range = list(range(max(current_page_nubmer - 2, 1), current_page_nubmer)) + \
                 list(range(current_page_nubmer, min(
                     current_page_nubmer + 2, paginator.num_pages) + 1))

    # 加省略号
    if page_range[0] - 1 >= 2:
        page_range.insert(0, "...")
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append("...")

    if page_range[0] != 1:
        page_range.insert(0, 1)
    if paginator.num_pages != page_range[-1]:
        page_range.append(paginator.num_pages)
    context = {}
    # 返回一页，10个数据
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    # 根据annotate给blogtype增加一个blog_count属性，统计这个blogtype对应了多少个博客
    context['BlogType'] = BlogType.objects.annotate(blog_count=Count('blog'))
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    # 根据日期分类统计博客的数量，blog_date这个对象作为字典的键，数量作为值
    blog_datesDic = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year, created_time__month=blog_date.month).count()
        blog_datesDic[blog_date] = blog_count

    context['blog_dates'] = blog_datesDic

    return context


def blog_list(request):
    blog_all_list = Blog.objects.all()
    context = blog_list_common_date(request, blog_all_list)

    return render(request, 'blog/blog_list.html', context)


def blogs_with_type(request, type_pk):
    blog_type = get_object_or_404(BlogType, pk=type_pk)
    blog_all_list = Blog.objects.filter(blog_type=blog_type)

    context = blog_list_common_date(request, blog_all_list)
    # 返回一页，10个数据
    context['blog_name'] = blog_type.get_type_name()
    return render(request, 'blog/blogs_with_type.html', context)


def blogs_with_date(request, year, month):
    blog_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = blog_list_common_date(request, blog_all_list)

    context['blog_date'] = "%s年%s月" % (year, month)
    return render(request, 'blog/blog_dates.html', context)


def blog_detail(request, blog_pk):
    context = {}
    blog = get_object_or_404(Blog, pk=blog_pk)
    key = read_num_once(request, blog)

    context['blog'] = blog
    context['loginform'] = LoginForm()
    context['blog_type'] = get_object_or_404(Blog, pk=blog_pk).blog_type.all()
    # 取时间大于当前博客创建的博客的集合，取最后一个
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    # 取时间小于当前博客创建的博客的集合，取第一个
    context['last_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    response = render(request, 'blog/blog_detail.html', context)
    response.set_cookie(key, 'true')
    return response
