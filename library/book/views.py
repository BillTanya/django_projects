from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from rest_framework import generics, viewsets
from rest_framework.response import Response

from .models import *
from order.models import Order
from author.models import Author
from.forms import *
from .serializers import BookSerializer

menu = [{'title': 'Home', 'url_name': 'home'},
        {'title': 'Users', 'url_name': 'users'},
        {'title': 'Orders', 'url_name': 'orders'},
        {'title': 'Books', 'url_name': 'books'},
        {'title': 'Authors', 'url_name': 'authors'}
        ]


def show_book_by_id(request, id):
    post = Book.objects.get(id=id)
    title = 'Information about book'
    context = {
        "menu": menu,
        "title": title,
        "post": post,
    }
    return render(request, 'book/book_by_id.html', context)

def book_filter(request):
    qs = Book.objects.all()
    name_query = request.GET.get('name')
    if name_query:
        qs = qs.filter(name__icontains=name_query)
    else:
        return redirect('books')
    # if count_query != "" and count_query is not None:
    #     qs = qs.filter(count__gte=count_query)

    title = 'Books'
    context = {
        "menu": menu,
        "title": title,
        "posts": qs,
    }
    return render(request, "book/all_books.html", context)



# def show_all_books(request):
#     title = 'Books:'
#     posts = []
#     for book in Book.objects.all():
#         try:
#             author = book.authors.get()
#             posts.append({'book': book, 'author': author})
#         except:
#             author = None
#             posts.append({'book': book, 'author': author})
#     context = {
#         "menu": menu,
#         "title": title,
#         "posts": posts,
#     }
#     return render(request, 'book/all_books.html', context)

class BookHome(ListView):
    paginate_by = 9
    model = Book
    template_name = 'book/all_books.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Books'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        a = Author.objects.all()
        authors = []
        for auth in a:
            if auth.books.all():
                authors.append(auth)
        authors.append('without author')
        books = Book.objects.all()
        context['menu'] = menu
        context['authors'] = authors
        context['books'] = books
        return context

    def get_queryset(self, **kwargs):
        no_aut = self.request.GET.getlist("noauthor")
        b_id = self.request.GET.getlist("id")
        a_id = self.request.GET.getlist("author")
        if b_id:
            book_id = int(b_id[0])
            return Book.objects.filter(id=book_id)
        elif a_id:
            author_id = int(a_id[0])
            return Book.objects.filter(authors__id=author_id)
        elif no_aut:
            posts = []
            for book in Book.objects.all():
                if not book.authors.all():
                    posts.append(book)
            return posts
        else:
            return Book.objects.all()


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer