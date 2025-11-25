from operator import is_
from django.contrib import admin, messages
from .models import Category, Tag, Product, ProductDetail, Review, ProductReaction
from django.utils.html import mark_safe

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
    save_on_top = True
    fields = ['name', 'slug', 'description', 'price', 'image', 'image_preview', 
    'category', 'tags', 'is_published']
    readonly_fields = ['image_preview']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductDetailInline]
    list_display = ('id', 'name', 'price', 'image_preview', 'category', 'created_at', 'is_published', 
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

    @admin.display(description='Изображение товара')
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-width: 100px; max-height: 100px;" />')
        return 'Нет изображения товара'

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


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at', 'text_preview']
    list_display_links = ['product']
    list_filter = ['rating', 'created_at', 'product__category']
    search_fields = ['product__name', 'user__username', 'text']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    ordering = ['-created_at']
    
    @admin.display(description='Текст отзыва')
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text


@admin.register(ProductReaction)
class ProductReactionAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'reaction_type_display', 'created_at']
    list_display_links = ['product']
    list_filter = ['reaction_type', 'created_at', 'product__category']
    search_fields = ['product__name', 'user__username']
    readonly_fields = ['created_at']
    list_per_page = 30
    ordering = ['-created_at']
    
    @admin.display(description='Реакция')
    def reaction_type_display(self, obj):
        return '👍 Нравится' if obj.reaction_type == 1 else '👎 Не нравится'
