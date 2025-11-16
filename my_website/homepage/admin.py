from django.contrib import admin, messages
from .models import Collection
from django.utils.html import mark_safe

# Register your models here.

# Регистрация моделей в админке
# Админка для модели Collection
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'image', 'image_preview', 'is_published']
    readonly_fields = ['image_preview']
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title', 'image_preview', 'time_create', 'is_published') 
    list_display_links = ('id', 'title')
    list_editable = ('is_published',)
    ordering = ['-time_create', 'title']
    list_filter = ('is_published',)
    list_per_page = 10
    actions = ('set_published', 'set_draft')
    search_fields = ('title__startswith',)

    @admin.display(description='Изображение коллекции')
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-width: 100px; max-height: 100px;" />')
        return 'Нет изображения коллекции'

    # Методы для действий в админке
    @admin.action(description='Опубликовать выбранные коллекции')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Collection.Status.PUBLISHED)
        self.message_user(request, f'Опубликовано {count} коллекции(й).')
    
    @admin.action(description='Снять с публикации выбранные коллекции')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Collection.Status.DRAFT)
        self.message_user(request, f'Снято с публикации {count} коллекции(й)!', messages.WARNING)
