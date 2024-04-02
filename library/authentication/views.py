from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from rest_framework.response import Response
from .models import *
from order.models import *
from django.views.generic import ListView, CreateView
from .forms import *
from rest_framework import generics, viewsets
from .serializers import UserSerializer


menu = [{'title': 'Home', 'url_name': 'home'},
        {'title': 'Users', 'url_name': 'users'},
        {'title': 'Orders', 'url_name': 'orders'},
        {'title': 'Books', 'url_name': 'books'},
        {'title': 'Authors', 'url_name': 'authors'}
        ]

class UserHome(ListView):
    paginate_by = 9
    model = CustomUser
    # queryset = CustomUser.objects.order_by('id')
    template_name = 'authentication/all_users.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Users'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['menu'] = menu
        return context

    def get_queryset(self, **kwargs):
        roles = {"librarian": 1, "visitor": 0}
        name_query = self.request.GET.getlist("name")
        role_query = self.request.GET.getlist("role")
        if name_query:
            name_query = name_query[0]
            return CustomUser.objects.filter(Q(first_name__icontains=name_query)
                                   | Q(middle_name__icontains=name_query)
                                   | Q(last_name__icontains=name_query)
                                   )
        elif role_query:
            role_query = role_query[0]
            if role_query != 'any':
                return CustomUser.objects.filter(role=roles[role_query])
            else:
                return CustomUser.objects.all()
        else:
            return CustomUser.objects.all()

# def show_inf_all_users(request):
#     title = 'Users'
#     posts = CustomUser.objects.all()
#     context = {
#            "menu": menu,
#            "title": title,
#            "posts": posts,
#        }
#     return render(request, 'authentication/all_users.html', context)


def show_user_by_id(request, id):
    post = CustomUser.objects.get(id=id)
    title = 'Information about user'
    books = Order.objects.filter(user_id=id, end_at=None)
    if books:
        if len(list(books)) > 1:
            last_book = list(books)[-1]
            books = books[::-1]
            books = books[1:]
            context = {
                "menu": menu,
                "title": title,
                "post": post,
                'books': books,
                'last_book': last_book
            }
        else:
            last_book = list(books)[-1]
            context = {
                "menu": menu,
                "title": title,
                "post": post,
                'books': None,
                'last_book': last_book
            }
    else:
        context = {
                "menu": menu,
                "title": title,
                "post": post,
                'books': None,
                'last_book': None
            }

    return render(request, 'authentication/user_by_id.html', context)


class RegisterUser(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('login')
    extra_context = {'title': 'Login form'}


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'authentication/login.html'
    extra_context = {'title': 'Login user', 'message': 'Authorization'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')

def home_page(request):
    title = "Please log in"
    context = {
               "menu": menu,
               "title": title,
           }
    return render(request, "authentication/home_page.html", context)


# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             try:
#                 CustomUserCreationForm.create(**form.cleaned_data)
#                 return redirect('authors')
#             except:
#                 form.add_error(None, 'Error')
#     else:
#         form = CustomUserCreationForm()
#     title = 'Register new user'
#     context = {
#         "menu": menu,
#         "title": title,
#         "form": form
#     }
#     return render(request, 'authentication/register.html', context)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


# class UserAPIList(generics.ListCreateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer
#
#
# # class UserAPIUpdate(generics.UpdateAPIView):
# #     queryset = CustomUser.objects.all()
# #     serializer_class = UserSerializer
#
#
# class UserAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer



# class UserAPIView(generics.ListAPIView):
#     serializer_class = UserSerializer
#     def get(self, request,  *args, **kwargs):
#         id = kwargs.get('id', None)
#         if id:
#             user = CustomUser.objects.filter(id=id)
#             return Response({'user': UserSerializer(user, many=True).data})
#         else:
#             users = CustomUser.objects.all()
#             return Response({'users': UserSerializer(users, many=True).data})
#
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'user': serializer.data})

    # def put(self, request, *args, **kwargs):
    #     id = kwargs.get('id', None)
    #     if not id:
    #         return Response({'error': "Method put not allowed"})
    #     try:
    #         instance = CustomUser.objects.get(id=id)
    #     except:
    #         return Response({'error': "Object does not exists"})
    #     serializer = UserSerializer(data=request.data, instance=instance)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response({'user': serializer.data})
    #
    # def delete(self, request, *args, **kwargs):
    #     id = kwargs.get('id', None)
    #     if not id:
    #         return Response({'error': "Method DELETE not allowed"})
    #     try:
    #         instance = CustomUser.objects.get(id=id)
    #         instance.delete()
    #     except:
    #         return Response({'error': "Object does not exists"})
    #     return Response({'user': f'User with id {id} was removed'})




