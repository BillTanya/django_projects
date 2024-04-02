from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .models import Women, Category
from .forms import *
from .utils import *



class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_super_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')

#def index(request):
#    posts = Women.objects.all()
#    #cats = Category.objects.all() #теперь мы эти данные берем из тега
#    context = {
#        "menu": menu,
#        #"cats": cats,
#        "title": "Главная страница",
#        "posts": posts,
#        "cat_selected": 0
#    }
#    return render(request, "women/index.html", context)

#@login_required декоратор для ограничения доступа для неавторизованных пользователей
def about(request):
    contact_list = Women.objects.all()
    #paginator = Paginator(contact_list, 3) # создаем экземпляр класса пагинатор,
    # указав ему столько объектов из списка выводить на странице
    #page_number = request.GET.get('page') # мы получаем номер текущей страницы с помощью GET запроса,
    # мы обращаемся к коллекции GET и берем атрибут, который должен быть записан в GET
    #page_obj = paginator.get_page(page_number) # объект, который содержит список элементов текущей страницы
    return render(request, "women/about.html", {"title": "О сайте"})

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/add_page.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_super_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))

#def add_page(request):
#    if request.method == "POST":
#        form = AddPostForm(request.POST, request.FILES)
#        if form.is_valid():
#            #try:
#                # Women.objects.create(**form.cleaned_data) мы сохраняли наши данные в БД
#                # с помощью распаковки словаря cleaned_data
#                # и передавали его методу create для того что бы создать новую запись
#            #except:
#                #form.add_error(None, 'Ошибка добавления посла')
#            form.save()  # строки выше были заменены методом save()
#            return redirect('home')
#    else:
#        form = AddPostForm()
#    return render(request, "women/add_page.html",
#                  {
#                      "menu": menu,
#                      "title": "Добавление статьи",
#                      "form": form
#                  })


class ContactFormView(DataMixin, FormView): # FormView - стандартная форма в джанго, которая не привязана к модели
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_super_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


#def contact(request):
    #return HttpResponse("Обратная связь")



#def login(request):
    #return HttpResponse("Войти")

class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'# по умолчанию используется 'slug'
    #pk_url_kwarg = 'post_pk' по умолчанию используется 'pk'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_super_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


#def show_post(request, post_slug):
#   post = get_object_or_404(Women, slug=post_slug)
#   context = {
#       "menu": menu,
#       "title": post.title,
#       "post": post,
#       "cat_selected": post.cat_id
#   }
#   return render(request, 'women/post.html', context)

class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_super_context(title='Категория - ' + str(c.name), cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))



#def show_category(request, cat_slug):
#    posts = Women.objects.filter(cat__slug=cat_slug)
#    #cats = Category.objects.all()  #теперь мы эти данные берем из тега
#    if len(posts) == 0:
#        raise Http404()
#    context = {
#        "posts": posts,
#        #"cats": cats,
#        "menu": menu,
#        "title": "Отображение по рубрикам",
#        "cat_selected": cat_slug
#    }
#    return render(request, "women/index.html", context)



#def archive(request, year):
#    if int(year) > 2020:
#        return redirect('home', permanent=True) # permanent=True для того что бы наш редирект был постоянным
#    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")


def page_notfound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_super_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_super_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
