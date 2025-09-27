"""
Контекстные процессоры для проекта my_website.
"""

SITE_NAME = 'BrandStack'

MENU = [
    {'title': 'Главная', 'url_name': 'homepage'},
    {'title': 'Каталог товаров', 'url_name': 'catalog'},
    {'title': 'Акции и скидки', 'url_name': 'promotions'},
    {'title': 'Контакты', 'url_name': 'contacts'},
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Войти', 'url_name': 'login'},
]

CONTACTS = [
    {'id': 1, 'name': 'Telegram', 'url_address': 'https://t.me/daniilqin'},
    {'id': 2, 'name': 'VK', 'url_address': 'https://vk.com/daniilqin'},
    {'id': 3, 'name': 'Email',
     'url_address': 'mailto:orlov.daniil.yu@gmail.com'},
]


def common_context(request):
    """
    Добавляет общий контекст для всех шаблонов.
    """
    return {
        'site_name': SITE_NAME,
        'menu': MENU,
        'contacts': CONTACTS,
    }
