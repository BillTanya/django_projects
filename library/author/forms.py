from django import forms
from .models import *
from book.models import Book


# class AddAuthorForm(forms.ModelForm):
#     class Meta:
#         model = Book
#         fields = '__all__'


class AddAuthorForm(forms.Form):
    name = forms.CharField(max_length=20, label="author's name", widget=forms.TextInput())
    surname = forms.CharField(max_length=20, label="author's surname", widget=forms.TextInput())
    patronymic = forms.CharField(max_length=20, label="author's patronymic", required=None, widget=forms.TextInput())


