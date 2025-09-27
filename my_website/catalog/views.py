from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseNotFound

from datetime import datetime as dt

# Create your views here.

categories_db = [
    {'name': 'Женская одежда', 'url_name': 'womens'},
    {'name': 'Мужская одежда', 'url_name': 'mens'},
    {'name': 'Детская одежда', 'url_name': 'kids'},
    {'name': 'Обувь', 'url_name': 'shoes'},
    {'name': 'Аксессуары', 'url_name': 'accessories'},
    {'name': 'Новинки', 'url_name': 'new'},
    {'name': 'Распродажа', 'url_name': 'sale'},
]


def catalog(request):
    data = {
        'title': 'Каталог',
    }
    return render(request, 'catalog/catalog.html', context=data)


def category_detail(request, category_slug):
    return HttpResponse(f'<h1>Категория - {category_slug}')


def item_detail(request, item_slug):
    try:
        numeric_slug = int(item_slug)
        if numeric_slug < 0:
            raise Http404()
    except ValueError:
        pass

    if request.GET:
        print(request.GET)

    return HttpResponse(f'<h1>Запрошен продукт - {item_slug}</h1>')


def event_detail(request, event_date):
    acceptable_date = '2026-01-01'

    if event_date > dt.strptime(acceptable_date, '%Y-%m-%d').date():
        return redirect('catalog', permanent=True)

    return HttpResponse(f'<h1>Дата события - {event_date}</h1>')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
