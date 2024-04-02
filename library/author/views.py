from django.shortcuts import render, redirect, Http404
from rest_framework import generics, viewsets
from rest_framework.response import Response
from .serializers import *
from .models import *
from order.models import *
from .forms import *
from django.views.generic import ListView
from book.views import *
from django.core.paginator import Paginator
from django.db.models import Q



menu = [{'title': 'Home', 'url_name': 'home'},
        {'title': 'Users', 'url_name': 'users'},
        {'title': 'Orders', 'url_name': 'orders'},
        {'title': 'Books', 'url_name': 'books'},
        {'title': 'Authors', 'url_name': 'authors'}
        ]

class AuthorHome(ListView):
    paginate_by = 9
    model = Author
    template_name = 'author/all_authors.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Authors'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['menu'] = menu
        return context

    def get_queryset(self, **kwargs):
        name = self.request.GET.getlist("name")
        if name:
            name = name[0]
            return Author.objects.filter(Q(name__icontains=name)| Q(surname__icontains=name))
        else:
            return Author.objects.all()



# def show_all_authors(request):
#     posts = []
#     authors = Author.objects.all()
#     last_book = None
#     for author in authors:
#         books = []
#         count = -1
#         for book in Book.objects.all():
#             for aut in book.authors.all():
#                 if author.id == aut.id:
#                     count += 1
#                     books.append(book)
#         if count > 0:
#             last_book = books[-1]
#             books.remove(books[-1])
#         posts.append({'author': author, 'books': books, 'count': count, 'last_book': last_book})
#     title = 'Authors'
#     context = {
#         "menu": menu,
#         "title": title,
#         "posts": posts,
#     }
#     return render(request, 'author/all_authors.html', context)



def show_author_by_id(request, id):
    post = Author.objects.get(id=id)
    title = 'Information about author'
    context = {
        "menu": menu,
        "title": title,
        "post": post,
    }
    return render(request, 'author/author_by_id.html', context)

def add_author(request):
    if request.method == 'POST':
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            try:
                Author.create(**form.cleaned_data)
                return redirect('authors')
            except:
                form.add_error(None, 'Error')
    else:
        form = AddAuthorForm()
    title = 'Add author'
    context = {
        "menu": menu,
        "title": title,
        "form": form
    }
    return render(request, 'author/add_author.html', context)



def delete_author_by_id(request, id):
    try:
        b = Author.delete_by_id(id)
        if b == True:
            return redirect('authors')
        else:
            raise ValueError
    except:
        return show_book_by_id(request, b.id)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = AuthorSerializer
