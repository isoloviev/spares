# Create your views here.
from django.http import HttpResponse


def list_news(request):
    return HttpResponse('Text message')