from django.shortcuts import render
from spares.dealers.models import Dealer


def index(request):
    list_items = Dealer.objects.all()
    return render(request, 'dealers/index.html', {
        'items': list_items,
    })


def details(request, code):
    item = Dealer.objects.get(code=code)
    return render(request, 'dealers/details.html', {
        'item': item,
    })