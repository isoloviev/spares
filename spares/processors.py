from spares.dealers.models import Dealer
from spares.models import CSpares
from spares.news.models import News


def display_news(request):
    list_news = News.objects.order_by('-pubDate')[:10]
    return {'display_news': list_news}


def display_dealers(request):
    list_dealers = Dealer.objects.all().order_by('?')[:10]
    return {'display_dealers': list_dealers}


def display_spares_models(request):
    list_models = CSpares.carModels.listRandomRecs(3)
    return {'display_spares_models': list_models}