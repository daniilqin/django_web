from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

data_db = [
    {'id': 1, 'title': 'The North Face',
     'content': 'Коллекция The North Face 2025', 'is_published': True},
    {'id': 2, 'title': 'Tommy Hilfiger',
     'content': 'Коллекция Tommy Hilfiger 2025', 'is_published': True},
    {'id': 3, 'title': 'Levis',
     'content': 'Коллекция Levis 2025', 'is_published': True},
    {'id': 4, 'title': 'Nike',
     'content': 'Коллекция Nike 2025', 'is_published': True},
]

categories_db = [
    {'id': 'womens', 'name': 'Женщинам'},
    {'id': 'mens', 'name': 'Мужчинам'},
    {'id': 'kids', 'name': 'Детям'},
]


def index(request):
    data = {
        'title': 'Главная',
        'new_collections': data_db,
    }
    return render(request, 'homepage/index.html', context=data)


def promotions(request):
    return HttpResponse('<h1>Акции и скидки</h1>')


def contacts(request):
    return HttpResponse('<h1>Контакты</h1>')


def about(request):
    data = {
        'title': 'О сайте',
    }
    return render(request, 'homepage/about.html', context=data)


def login(request):
    return HttpResponse('<h1>Войти</h1>')


def show_category(request, category_slug):
    return HttpResponse(f'<h1>Категория - {category_slug}</h1>')


def show_collection(request, collection_slug):
    return HttpResponse(f'<h1>Коллекция - {collection_slug}</h1>')
