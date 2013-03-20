from django.contrib import admin
from spares.news.models import News

class NewsAdmin(admin.ModelAdmin):
    list_display = ('pubDate', 'title', 'webSite')
    list_filter = ('webSite',)

admin.site.register(News, NewsAdmin)