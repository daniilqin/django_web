from django.db import models
from django.urls import reverse

# Create your models here.


class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Product.Status.PUBLISHED)


class Tag(models.Model):
    """Теги для товаров"""
    name = models.CharField(max_length=100, verbose_name="Название тега")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL")
    
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        # ordering = ['name']
    
    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})
    
    def __str__(self):
        return self.name


class Category(models.Model):
    """Категории товаров (Женская одежда, Мужская одежда, Обувь и т.д.)"""
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        # ordering = ['name']
    
    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Базовая модель товара"""

    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    name = models.CharField(max_length=255, verbose_name="Название товара")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(verbose_name="Описание товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='products/%Y/%m/%d/', default=None, null=True, 
                              blank=True, verbose_name="Изображение товара")
    
    # Связь Many-to-One: один товар принадлежит одной категории
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True, 
                                related_name='products', verbose_name="Категория")
    
    # Связь Many-to-Many: товар может иметь много тегов, тег может быть у многих товаров
    tags = models.ManyToManyField(Tag, blank=True, related_name='products', verbose_name="Теги")

    # Статус и даты
    is_published = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
        default=Status.DRAFT,
        verbose_name="Опубликовано"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    objects = models.Manager()       # стандартный менеджер
    published = PublishedModel()   # наш кастомный менеджер

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at']),]
        permissions = [
            ('can_publish_product', "Может публиковать и снимать товар с публикации"),
        ]

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})

    def __str__(self):
        return self.name


class ProductDetail(models.Model):
    """Дополнительная информация о товаре (связь Один-к-Одному)"""
    
    # Связь Один-к-Одному: каждый товар имеет одну детальную информацию
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True, 
                                    related_name='detail', verbose_name="Товар")
    
    # Размеры и характеристики
    size = models.CharField(max_length=50, blank=True, verbose_name="Размер")
    material = models.CharField(max_length=100, blank=True, verbose_name="Материал")
    color = models.CharField(max_length=50, blank=True, verbose_name="Цвет")
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True,
                               verbose_name="Вес (кг)")
    
    # Информация об уходе
    care_instructions = models.TextField(blank=True, verbose_name="Инструкции по уходу")
    
    # Дополнительные характеристики
    manufacturer = models.CharField(max_length=100, blank=True, verbose_name="Производитель")
    country_origin = models.CharField(max_length=50, blank=True, verbose_name="Страна производства")
    production_year = models.PositiveIntegerField(null=True, blank=True, verbose_name="Год производства")
    warranty_period = models.CharField(max_length=50, blank=True, verbose_name="Гарантийный срок")
    
    # Складская информация
    sku = models.CharField(max_length=50, blank=True, verbose_name="Артикул")
    barcode = models.CharField(max_length=50, blank=True, verbose_name="Штрих-код")
    
    class Meta:
        verbose_name = "Детальная информация о товаре"
        verbose_name_plural = "Детальная информация о товарах"
    
    def __str__(self):
        return f"Детали: {self.product.name}"
