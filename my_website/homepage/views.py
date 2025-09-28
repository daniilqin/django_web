from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Collection

# Create your views here.

categories_db = [
    {'id': 'womens', 'name': 'Женщинам'},
    {'id': 'mens', 'name': 'Мужчинам'},
    {'id': 'kids', 'name': 'Детям'},
]


def index(request):
    # Получаем коллекции из базы данных (только опубликованные)
    new_collections = Collection.published.all()

    # Получаем коллекции из базы данных (все)
    # new_collections = Collection.objects.all()

    data = {
        'title': 'Главная',
        'new_collections': new_collections,
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
    collection = get_object_or_404(Collection, slug=collection_slug)
    data = {
        'title': collection.title,
        'collection': collection,
    }
    return render(request, 'homepage/collection.html', context=data)
