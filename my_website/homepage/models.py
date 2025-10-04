from django.db import models
from django.urls import reverse

# Create your models here.


class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Collection.Status.PUBLISHED)


class Collection(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name="Название коллекции")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to='collections/', blank=True, null=True, verbose_name="Изображение коллекции")
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT, verbose_name="Опубликовано")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")

    objects = models.Manager()       # стандартный менеджер
    published = PublishedModel()   # наш кастомный менеджер

    class Meta:
        ordering = ['-time_create'] 
        indexes = [models.Index(fields=['-time_create']),]

    def get_absolute_url(self):
        return reverse('collection', kwargs={'collection_slug': self.slug})

    def __str__(self):
        return self.title
