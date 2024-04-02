from django import forms
from .models import Book
from author.models import Author


class FilterNameBookForm(forms.Form):
    book_name = forms.ModelChoiceField(queryset=Book.objects.all(), label='filter by name')


class FilterNameAuthorForm(forms.Form):
    author_name = forms.ModelChoiceField(queryset=Author.objects.all())

"""class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, label="Заголовок", widget=forms.TextInput(attrs={'class': 'form-input'}))
    slug = forms.SlugField(max_length=255, label="URL")
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label="Контент")
    is_published = forms.BooleanField(label="Публикация", initial=True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категории", empty_label="Категория не выбрана")
"""