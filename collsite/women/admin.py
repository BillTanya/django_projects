from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Women, Category


class WomenAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'time_create', 'get_html_photo', 'is_published']
    list_display_links = ['id', 'title']
    search_fields = ('title', 'content',)
    list_editable = ['is_published']
    list_filter = ['is_published', 'time_create']
    prepopulated_fields = {"slug": ("title",)}
    fields = ['title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update']
    readonly_fields = ['time_create', 'time_update', 'get_html_photo']
    save_on_top = True # кнопочки сохранить/удалить запись появятся вверху, если впадло прокручивать вниз

    def get_html_photo(self, object): # метод для отображения фото в админ панели вместо ссылки|
        # object нестандартный параметр, а дополнительный, он будет ссылаться на текущую запись списка.
        # будет ссылаться на объект модели Women
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=40>") # функция mark_safe указывает не экранировать символы

    get_html_photo.short_description = 'Миниатюра' # меняем название поля в админке

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)



