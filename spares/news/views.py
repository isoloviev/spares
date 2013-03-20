# Create your views here.
from django.shortcuts import render

from spares.news.models import News


def render_view(request, list_news):
    return render(request, 'news/index.html', {
        'list_news': list_news,
    })


def index(request):
    return render_view(request, News.objects.order_by('-pubDate')[:10])


def year_archive(request, year):
    return render_view(request, News.objects.filter(pubDate__year=year).order_by('-pubDate')[:10])


def month_archive(request, year, month):
    return render_view(request, News.objects.filter(pubDate__year=year, pubDate__month=month).order_by('-pubDate')[:10])


def day_archive(request, year, month, day):
    return render_view(request, News.objects.filter(pubDate__year=year,
                                                    pubDate__month=month,
                                                    pubDate__day=day).order_by('-pubDate')[:10])


def details(request, year, month, day, id):
    news_item = News.objects.get(id=id)
    return render(request, 'news/details.html', {
        'item': news_item,
    })

