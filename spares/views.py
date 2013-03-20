# coding=utf-8
import json
from django.http import HttpResponse
from django.shortcuts import render
from spares import settings
from spares.models import CSpares

__author__ = 'ivans'


def home(request):
    list_models = []
    for letter in ['1', '3', '5', 'X']:
        by_letter = CSpares.carModels.listByLetter(letter)
        list_models.append([letter, by_letter])

    return render(request, 'home.html', {
        'list_models': list_models
    })


def contacts(request):
    return render(request, 'contacts.html')


def models_list(request):
    list_models = []
    for letter in settings.TD_ALHPABET:
        by_letter = CSpares.carModels.listByLetter(letter)
        list_models.append([letter, by_letter])

    return render(request, 'spares/models_list.html', {
        'list_models': list_models,
        'brand': 'BMW'  # todo need to get from web site settings
    })


def variants_list(request, model):
    model = CSpares.carModels.findByTitle(model)
    list_variants = CSpares.carVariants.list(model.id)
    list_rnd_models = CSpares.carModels.listRandomRecs(18)
    return render(request, 'spares/variants_list.html', {
        'carModel': model,
        'list_variants': list_variants,
        'list_rnd_models': list_rnd_models
    })


def applies_list(request, model, typ_id):
    model = CSpares.carModels.findByTitle(model)
    carVariant = CSpares.carVariants.findById(model.id, typ_id)

    return render(request, 'spares/applies_list.html', {
        'carModel': model,
        'carVariant': carVariant,
    })


def spares_list(request, model, typ_id, str_id):
    model = CSpares.carModels.findByTitle(model)
    carVariant = CSpares.carVariants.findById(model.id, typ_id)
    strData = CSpares.strTree.getById(typ_id, str_id)
    list_spares = CSpares.items.list(typ_id, str_id)

    return render(request, 'spares/spares_list.html', {
        'carModel': model,
        'carVariant': carVariant,
        'str': strData,
        'list_spares': list_spares
    })


def spares_load(request):
    list_str = CSpares.strTree.list(request.GET.get('typ_id', 0), request.GET.get('str_id', 0))
    prep = []
    for item in list_str:
        prep.append({'name': item['text'],
                     'type': ('folder' if item['leaf'] == 1 else 'item'),
                     'additionalParameters': {'id': 'node%s' % item['id'], 'url': '%s/' % item['id']}})
    jsonObject = json.dumps({'data': prep})
    return HttpResponse(jsonObject, mimetype="application/json")


def article_info(request, article):
    article = str(article)
    if article.endswith('/'):
        article = article[:len(article) - 1]
    article = CSpares.items.getById(article.replace('_', ' '))
    criteries = CSpares.items.criteries(article.id)
    images = CSpares.items.images(article.id)
    applicables = CSpares.items.applicables(article.id)

    return render(request, 'spares/article.html', {
        'item': article,
        'criteries': criteries,
        'images': images,
        'applicables': applicables
    })