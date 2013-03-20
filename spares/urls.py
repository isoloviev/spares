from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'spares.views.home', name='home'),
    url(r'^contacts/$', 'spares.views.contacts', name='contacts'),
    url(r'^spares-load/$', 'spares.views.spares_load', name='spares_load'),

    url(r'^news/$', 'spares.news.views.index'),
    url(r'^news/(\d{4})/$', 'spares.news.views.year_archive'),
    url(r'^news/(\d{4})/(\d{2})/$', 'spares.news.views.month_archive'),
    url(r'^news/(\d{4})/(\d{2})/(\d{2})/$', 'spares.news.views.day_archive'),
    url(r'^news/(\d{4})/(\d{2})/(\d{2})/(\d+)/$', 'spares.news.views.details', name='news-details'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^spares/$', 'spares.views.models_list'),
    url(r'^spares/article/(.+)$', 'spares.views.article_info'),
    url(r'^spares/([^/]+)/$', 'spares.views.variants_list'),
    url(r'^spares/([^/]+)/(\d+)/$', 'spares.views.applies_list', name='applies-list'),
    url(r'^spares/([^/]+)/(\d+)/(\d+)/$', 'spares.views.spares_list'),

    url(r'^dealers/$', 'spares.dealers.views.index'),
    url(r'^dealers/([^/]+)/$', 'spares.dealers.views.details', name='dealers-details'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
