from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.views import View
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy

from datetime import datetime as dt
from .models import Product, Category, Tag, ProductReaction
from .forms import AddProductForm, AddProductModelForm, UploadFileForm, ReviewForm
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
class ProductView(PermissionRequiredMixin, LoginRequiredMixin, CatalogContextMixin, DetailView):
    model = Product
    template_name = 'catalog/product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'
    page_title = 'Каталог'
    permission_required = 'catalog.view_product'
    
    def get_queryset(self):
        return Product.published.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        # Получаем отзывы для товара
        reviews = product.reviews.all()
        
        # Проверяем, оставлял ли текущий пользователь отзыв
        user_has_review = False
        if self.request.user.is_authenticated:
            user_has_review = reviews.filter(user=self.request.user).exists()
        
        # Добавляем форму для отзыва
        review_form = ReviewForm()
        
        # Получаем счетчики реакций
        likes_count = product.reactions.filter(reaction_type=ProductReaction.ReactionType.LIKE).count()
        dislikes_count = product.reactions.filter(reaction_type=ProductReaction.ReactionType.DISLIKE).count()
        
        # Получаем реакцию текущего пользователя
        user_reaction = None
        if self.request.user.is_authenticated:
            try:
                user_reaction = product.reactions.get(user=self.request.user).reaction_type
            except ProductReaction.DoesNotExist:
                user_reaction = None
        
        context.update({
            'reviews': reviews,
            'user_has_review': user_has_review,
            'review_form': review_form,
            'reviews_count': reviews.count(),
            'likes_count': likes_count,
            'dislikes_count': dislikes_count,
            'user_reaction': user_reaction,
        })
        
        return self.get_mixin_context(context)


# Добавление отзыва к товару
class AddReviewView(LoginRequiredMixin, View):
    """View для добавления отзыва к товару"""
    
    def post(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug, is_published=True)
        
        # Проверяем, не оставлял ли пользователь уже отзыв
        if product.reviews.filter(user=request.user).exists():
            return redirect('product', product_slug=product_slug)
        
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product', product_slug=product_slug)
        
        # Если форма невалидна, возвращаемся на страницу товара с ошибками
        context = {
            'product': product,
            'reviews': product.reviews.all(),
            'review_form': form,
            'user_has_review': False,
            'reviews_count': product.reviews.count(),
        }
        return render(request, 'catalog/product.html', context)


# Добавление/изменение реакции на товар (лайк/дизлайк)
class ProductReactionView(LoginRequiredMixin, View):
    """View для добавления или изменения реакции на товар"""
    
    def post(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug, is_published=True)
        reaction_type = request.POST.get('reaction_type')
        
        # Валидация типа реакции
        if reaction_type not in ['1', '-1']:
            return redirect('product', product_slug=product_slug)
        
        reaction_type = int(reaction_type)
        
        # Получаем существующую реакцию пользователя или создаем новую
        reaction, created = ProductReaction.objects.get_or_create(
            product=product,
            user=request.user,
            defaults={'reaction_type': reaction_type}
        )
        
        # Если реакция уже существовала
        if not created:
            # Если нажали на ту же кнопку - удаляем реакцию
            if reaction.reaction_type == reaction_type:
                reaction.delete()
            # Если нажали на другую кнопку - меняем реакцию
            else:
                reaction.reaction_type = reaction_type
                reaction.save()
        
        return redirect('product', product_slug=product_slug)


# Добавление товара через форму, связанную с моделью (используется в проекте)
class AddProductView(PermissionRequiredMixin, LoginRequiredMixin, CatalogContextMixin, CreateView):
    model = Product
    form_class = AddProductModelForm
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('catalog')
    page_title = 'Добавление товара'
    permission_required = 'catalog.add_product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


# Редактирование товара
class UpdateProductView(PermissionRequiredMixin, LoginRequiredMixin, CatalogContextMixin, UpdateView):
    model = Product
    form_class = AddProductModelForm
    template_name = 'catalog/add_product.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'
    page_title = 'Редактирование товара'
    permission_required = 'catalog.change_product'
    
    def get_success_url(self):
        return reverse_lazy('product', kwargs={'product_slug': self.object.slug})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, is_edit=True)


# Удаление товара
class DeleteProductView(PermissionRequiredMixin, LoginRequiredMixin, CatalogContextMixin, DeleteView):
    model = Product
    template_name = 'catalog/confirm_delete.html'
    slug_url_kwarg = 'product_slug'
    success_url = reverse_lazy('catalog')
    context_object_name = 'product'
    page_title = 'Удаление товара'
    permission_required = 'catalog.delete_product'
    
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
