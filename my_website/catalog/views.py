from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.views import View
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from datetime import datetime as dt
from .models import Product, Category, Tag
from .forms import AddProductForm, AddProductModelForm, UploadFileForm
from .utils import CatalogContextMixin
import uuid

# Create your views here.


# Каталог товаров
class CatalogView(CatalogContextMixin, ListView):
    model = Product
    template_name = 'catalog/catalog.html'
    context_object_name = 'products'
    page_title = 'Каталог'
    
    def get_queryset(self):
        return Product.published.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, category=None)


# Показ товаров категории
class CategoryView(CatalogContextMixin, ListView):
    model = Product
    template_name = 'catalog/catalog.html'
    context_object_name = 'products'
    page_title = 'Каталог'
    
    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return Product.published.filter(category=category)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return self.get_mixin_context(context, category=category)


# Показ товаров с тегом
class TagView(CatalogContextMixin, ListView):
    model = Product
    template_name = 'catalog/catalog.html'
    context_object_name = 'products'
    page_title = 'Каталог'
    
    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        return Product.published.filter(tags=tag)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, tag=tag)


# Показ товара
class ProductView(CatalogContextMixin, DetailView):
    model = Product
    template_name = 'catalog/product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'
    page_title = 'Каталог'
    
    def get_queryset(self):
        return Product.published.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


# Добавление товара через форму, связанную с моделью (используется в проекте)
class AddProductView(LoginRequiredMixin, CatalogContextMixin, CreateView):
    model = Product
    form_class = AddProductModelForm
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('catalog')
    page_title = 'Добавление товара'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


# Редактирование товара
class UpdateProductView(LoginRequiredMixin, CatalogContextMixin, UpdateView):
    model = Product
    form_class = AddProductModelForm
    template_name = 'catalog/add_product.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'
    page_title = 'Редактирование товара'
    
    def get_success_url(self):
        return reverse_lazy('product', kwargs={'product_slug': self.object.slug})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, is_edit=True)


# Удаление товара
class DeleteProductView(LoginRequiredMixin, CatalogContextMixin, DeleteView):
    model = Product
    template_name = 'catalog/confirm_delete.html'
    slug_url_kwarg = 'product_slug'
    success_url = reverse_lazy('catalog')
    context_object_name = 'product'
    page_title = 'Удаление товара'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


# Загрузка файла
class UploadFileView(LoginRequiredMixin, CatalogContextMixin, FormView):
    form_class = UploadFileForm
    template_name = 'catalog/upload_file.html'
    success_url = reverse_lazy('catalog')
    page_title = 'Загрузка файла'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)
    
    def form_valid(self, form):
        handle_uploaded_file(form.cleaned_data['file'])
        return super().form_valid(form)


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
