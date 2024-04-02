from django.db.models import Count
from django.core.cache import cache

from .models import *


menu = [{"title": "О сайте", "url_name": "about"},
        {"title": "Добавить статью", "url_name": "add_page"},
        {"title": "Обратная связь", "url_name": "contact"}]

class DataMixin:
    paginate_by = 3

    def get_super_context(self, **kwargs):
        context = kwargs
        cats = cache.get('cats') # пытаемся получить данные из кеша
        if not cats: # если данных нет, None
            cats = Category.objects.annotate(Count('women')) # Мы будем брать данные из БД
            cache.set('cats', cats, 60) # по ключу 'cats' мы будем заносить коллекцию cats и указываем на сколько ее сохраняем

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)
        context['menu'] = user_menu
        context['cats'] = cats
        if "cat_selected" not in context:
            context["cat_selected"] = 0
        return context
