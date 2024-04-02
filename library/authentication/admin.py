from django.contrib import admin
from .models import *
from author.models import Author
from book.models import *
from order.models import *


class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'display_authors', 'count']
    list_display_links = ['id', 'name', 'display_authors', 'count']
    search_fields = ('id', 'name')
    list_filter = ['id', 'name', 'authors']
    save_on_top = True

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'surname', 'display_books', 'patronymic']
    list_display_links = ['id', 'name', 'surname', 'display_books']
    search_fields = ('id', 'name', )
    list_filter = ['id', 'name', 'books']
    save_on_top = True


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'middle_name', 'email', 'created_at', 'updated_at',
                    'role', 'is_active', 'is_staff']
    list_display_links = ['id', 'first_name', 'last_name', 'middle_name', 'email', 'created_at', 'updated_at']
    search_fields = ('id', 'first_name', 'last_name')
    list_filter = ['id', 'first_name', 'email', 'is_staff']
    save_on_top = True


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'user', 'created_at', 'plated_end_at', 'end_at']
    list_display_links = ['id', 'book', 'user', 'created_at', 'plated_end_at', 'end_at']
    search_fields = ('id',)
    list_filter = ['id', 'book', 'user', 'created_at']
    save_on_top = True

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Order, OrderAdmin)