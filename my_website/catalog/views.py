from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseNotFound

from datetime import datetime as dt
from .models import Product, Category, Tag
from .forms import AddProductForm, AddProductModelForm, UploadFileForm
import uuid

# Create your views here.

# Каталог
def catalog(request):
    # Получаем все опубликованные товары
    products = Product.published.all()
    
    data = {
        'title': 'Каталог',
        'category': None,
        'products': products,
    }
    return render(request, 'catalog/catalog.html', context=data)

# Показ категории
def show_category(request, category_slug):
    # Получаем категорию по slug
    category = get_object_or_404(Category, slug=category_slug)
    
    # Получаем товары этой категории (связь Many-to-One)
    products = Product.published.filter(category=category)
    
    data = {
        'title': 'Каталог',
        'category': category,
        'products': products,
    }
    return render(request, 'catalog/catalog.html', context=data)

# Показ тега
def show_tag(request, tag_slug):
    # Получаем тег по slug
    tag = get_object_or_404(Tag, slug=tag_slug)
    
    # Получаем товары с этим тегом (связь Many-to-Many)
    products = Product.published.filter(tags=tag)
    
    data = {
        'title': 'Каталог',
        'tag': tag,
        'products': products,
    }
    return render(request, 'catalog/catalog.html', context=data)

# Показ товара
def show_product(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    data = {
        'title': 'Каталог',
        'product': product,
    }
    return render(request, 'catalog/product.html', context=data)

# Добавление товара через форму, связанную с моделью (используется в проекте)
def add_product(request):
    if request.method == 'POST':
        form = AddProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog')
    else:
        form = AddProductModelForm()

    data = {
        'title': 'Добавить товар',
        'form': form,
    }

    return render(request, 'catalog/add_product.html', context=data)

# Загрузка файла
def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(form.cleaned_data['file'])
            return redirect('catalog')
    else:
        form = UploadFileForm()

    data = {
        'title': 'Загрузка файла',
        'form': form,
    }

    return render(request, 'catalog/upload_file.html', context=data)

# Сохранение загруженного файла
def handle_uploaded_file(f):
    name = f.name
    ext = ''

    if '.' in name: 
        ext = name[name.rindex('.'):] 
        name = name[:name.rindex('.')]

    suffix = str(uuid.uuid4())
    with open(f"uploads/{name}_{suffix}{ext}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

# Добавление товара через форму, несвязанную с моделью (не используется в проекте)
# def add_product(request):
#     if request.method == 'POST':
#         form = AddProductForm(request.POST)
#         if form.is_valid():
#             try:
#                 # Извлекаем теги из cleaned_data
#                 tags = form.cleaned_data.pop('tags')
#                 # Создаем товар без тегов
#                 product = Product.objects.create(**form.cleaned_data)
#                 # Добавляем теги через .set()
#                 if tags:
#                     product.tags.set(tags)
                    
#                 return redirect('catalog')
#             except Exception as e:
#                 form.add_error(None, f'Ошибка при добавлении товара: {e}')
#     else:
#         form = AddProductForm()
    
#     data = {
#         'title': 'Добавить товар',
#         'form': form,
#     }
    
#     return render(request, 'catalog/add_product.html', context=data)


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
