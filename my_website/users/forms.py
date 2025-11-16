from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model

import datetime


# Форма авторизации пользователя
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя (или E-mail)',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Введите имя пользователя (или E-mail)'
        }),
    )

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Введите пароль'
        }),
    )
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


# Форма регистрации нового пользователя
class RegisterUserForm(UserCreationForm):
    
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Введите имя пользователя'
        }),
    )

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Введите пароль'
        }),
    )

    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Подвердите пароль'
        }),
    )

    photo = forms.ImageField(
        label='Фотография профиля',
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-input'
        })
    )
    
    this_year = datetime.date.today().year
    max_year = this_year - 6
    date_birth = forms.DateField(
        label='Дата рождения',
        required=False,
        initial=datetime.date(max_year, datetime.date.today().month, datetime.date.today().day),
        widget=forms.SelectDateWidget(years=tuple(range(this_year-100, this_year-5)))
    )

    class Meta:
        model = get_user_model()
        fields = ['photo', 'username', 'email', 'first_name',
                  'last_name', 'date_birth', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'email': forms.TextInput(attrs={
                        'class': 'form-input',
                        'placeholder': 'Введите E-mail'
                     }),

            'first_name': forms.TextInput(attrs={
                            'class': 'form-input',
                            'placeholder': 'Введите имя'
                          }),

            'last_name': forms.TextInput(attrs={
                            'class': 'form-input',
                            'placeholder': 'Введите фамилию'
                         }),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким E-mail уже существует.")
        return email


# Форма редактирования профиля пользователя
class ProfileUserForm(forms.ModelForm):
    
    username = forms.CharField(disabled=True, label='Имя пользователя', 
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Введите имя пользователя'
        }))

    email = forms.CharField(disabled=True, label='E-mail', 
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Введите E-mail'
        }))
    
    date_joined = forms.DateTimeField(
        disabled=True,
        label='Дата регистрации',
        widget=forms.DateInput(attrs={'class': 'form-input'}, format='%d.%m.%Y')
    )
    
    this_year = datetime.date.today().year
    date_birth = forms.DateField(
        label='Дата рождения',
        required=False,
        widget=forms.SelectDateWidget(years=tuple(range(this_year-100, this_year-5)))
    )
    
    photo = forms.ImageField(
        label='Фотография профиля',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = get_user_model()
        fields = ['photo', 'username', 'email', 'first_name', 'last_name', 'date_birth', 'date_joined']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                            'class': 'form-input',
                            'placeholder': 'Введите имя'
                          }),

            'last_name': forms.TextInput(attrs={
                            'class': 'form-input',
                            'placeholder': 'Введите фамилию'
                         }),
        }


# Форма смены пароля пользователя
class UserPasswordChangeForm(PasswordChangeForm):

    old_password = forms.CharField(
        label='Текущий пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Введите текущий пароль'
        })
    )

    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Введите новый пароль'
        })
    )

    new_password2 = forms.CharField(
        label='Подтверждение нового пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Введите новый пароль'
        })
    )
