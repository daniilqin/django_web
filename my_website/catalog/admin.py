from operator import is_
from django.contrib import admin, messages
from .models import Category, Tag, Product, ProductDetail

# Register your models here.

# Фильтр для ценового диапазона
class PriceRangeFilter(admin.SimpleListFilter):
    title = 'Ценовой диапазон'
    parameter_name = 'price_range'

    def lookups(self, request, model_admin):
        return (
            ('low', 'До 1000 руб.'),
            ('medium', '1000-5000 руб.'),
            ('high', '5000-10000 руб.'),
            ('expensive', 'Свыше 10000 руб.'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(price__lt=1000)
        if self.value() == 'medium':
            return queryset.filter(price__gte=1000, price__lt=5000)
        if self.value() == 'high':
            return queryset.filter(price__gte=5000, price__lt=10000)
        if self.value() == 'expensive':
            return queryset.filter(price__gte=10000)

# Регистрация моделей в админке
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

# Inline админка для отображения ProductDetail в Product
class ProductDetailInline(admin.StackedInline):
    model = ProductDetail
    extra = 1

# Админка для модели Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'slug', 'description', 'price', 'category', 'tags', 'is_published']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductDetailInline]
    list_display = ('id', 'name', 'price', 'category', 'created_at', 'is_published', 
    'name_length', 'is_expensive')
    list_display_links = ('id', 'name')
    list_editable = ('price', 'is_published',)
    ordering = ['-created_at', 'name']
    list_filter = ('category__name', 'is_published', PriceRangeFilter)
    list_per_page = 10
    actions = ('set_published', 'set_draft')
    search_fields = ('name__startswith', 'category__name')
    filter_horizontal = ['tags']

    # Методы для отображения в админке
    @admin.display(description='Длина названия')
    def name_length(self, obj):
        return f'{len(obj.name)} символов'

    @admin.display(boolean=True, description='Дорогой товар')
    def is_expensive(self, obj):
        return obj.price > 10000

    # Методы для действий в админке
    @admin.action(description='Опубликовать выбранные товары')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Product.Status.PUBLISHED)
        self.message_user(request, f'Опубликовано {count} товара(ов).')
    
    @admin.action(description='Снять с публикации выбранные товары')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Product.Status.DRAFT)
        self.message_user(request, f'Снято с публикации {count} товара(ов)!', messages.WARNING)


@admin.register(ProductDetail)
class ProductDetailAdmin(admin.ModelAdmin):
    fields = ['size', 'material', 'color', 'weight', 'care_instructions', 'manufacturer', 
    'country_origin', 'production_year', 'warranty_period', 'sku', 'barcode']
    list_display = ['product', 'size', 'material', 'color', 'weight']
    list_display_links = ['product']
    list_filter = ['product__category__name', 'product__is_published']
    list_per_page = 10
    search_fields = ('product__name__startswith', 'product__category__name')
