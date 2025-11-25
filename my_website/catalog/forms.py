from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
import re
from .models import Product, Category, Tag, ProductDetail, Review

class AddProductForm(forms.Form):
    """Форма для добавления товара, не связанная с моделью"""
    """Форма не используется в проекте"""
    
    name = forms.CharField(
        max_length=255,
        label='Название товара',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите название товара',
        }),
        validators=[
            MinLengthValidator(5, message='Название товара должно быть не менее 5 символов.'),
            MaxLengthValidator(255, message='Название товара должно быть не более 255 символов.'),
        ]
    )
    
    slug = forms.SlugField(
        max_length=255,
        label='URL-адрес',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'url-adres-tovara'
        }),
        validators=[
            MinLengthValidator(5, message='URL-адрес должен быть не менее 5 символов.'),
            MaxLengthValidator(255, message='URL-адрес должен быть не более 255 символов.'),
        ]
    )
    
    description = forms.CharField(
        label='Описание',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Описание товара'
        }),
        validators=[
            MinLengthValidator(10, message='Описание товара должно быть не менее 10 символов.'),
            MaxLengthValidator(500, message='Описание товара должно быть не более 500 символов.'),
        ]
    )
    
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label='Цена (руб.)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': '0.00'
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Категория',
        required=False,
        empty_label='Выберите категорию',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        label='Теги',
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )
    
    is_published = forms.BooleanField(
        label='Опубликовать',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if re.search(r'[!@#$%^&*()+=\[\]{};:"\\|<>/?]', name):
            raise forms.ValidationError('Название товара не должно содержать специальные символы (!@#$%^&* и т.д.).')
        return name
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError('Цена товара должна быть не менее 0 рублей.')
        if price > 10000000:
            raise forms.ValidationError('Цена товара должна быть не более 10 000 000 рублей.')
        return price


class AddProductModelForm(forms.ModelForm):
    """Форма для добавления товара, связанная с моделью"""
    """Форма используется в проекте"""
    
    class Meta:
        model = Product
        fields = ['name', 'slug', 'description', 'price', 'image', 'category', 'tags', 'is_published']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название товара',
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'url-adres-tovara'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание товара'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.CheckboxSelectMultiple(),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Название товара',
            'slug': 'URL-адрес',
            'description': 'Описание',
            'price': 'Цена (руб.)',
            'image': 'Изображение товара',
            'category': 'Категория',
            'tags': 'Теги',
            'is_published': 'Опубликовать',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Делаем некоторые поля необязательными
        self.fields['category'].required = False
        self.fields['category'].empty_label = 'Выберите категорию'
        self.fields['tags'].required = False
        self.fields['is_published'].required = False
        self.fields['is_published'].initial = True

        # Добавляем валидаторы
        self.fields['name'].validators = [
            MinLengthValidator(5, message='Название товара должно быть не менее 5 символов.'),
            MaxLengthValidator(255, message='Название товара должно быть не более 255 символов.'),
        ]
        self.fields['slug'].validators = [
            MinLengthValidator(5, message='URL-адрес должен быть не менее 5 символов.'),
            MaxLengthValidator(255, message='URL-адрес должен быть не более 255 символов.'),
        ]
        self.fields['description'].validators = [
            MinLengthValidator(10, message='Описание товара должно быть не менее 10 символов.'),
            MaxLengthValidator(500, message='Описание товара должно быть не более 500 символов.'),
        ]
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if re.search(r'[!@#$%^&*()+=\[\]{};:"\\|<>/?]', name):
            raise forms.ValidationError('Название товара не должно содержать специальные символы (!@#$%^&* и т.д.).')
        return name
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError('Цена товара должна быть не менее 0 рублей.')
        if price > 10000000:
            raise forms.ValidationError('Цена товара должна быть не более 10 000 000 рублей.')
        return price

# Форма для загрузки файла
class UploadFileForm(forms.Form):
    file = forms.FileField(label='Файл')


# Форма для добавления отзыва
class ReviewForm(forms.ModelForm):
    """Форма для добавления отзыва к товару"""
    
    text = forms.CharField(
        label='Ваш отзыв',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Поделитесь своим мнением о товаре...',
            'rows': 4,
        }),
        validators=[
            MinLengthValidator(10, message='Отзыв должен содержать не менее 10 символов.'),
            MaxLengthValidator(1000, message='Отзыв должен содержать не более 1000 символов.'),
        ]
    )
    
    rating = forms.ChoiceField(
        label='Оценка',
        choices=Review.Rating.choices,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    
    class Meta:
        model = Review
        fields = ['text', 'rating']
    
    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text or text.strip() == '':
            raise forms.ValidationError('Отзыв не может быть пустым.')
        return text.strip()
