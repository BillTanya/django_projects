from datetime import datetime
from rest_framework import serializers
from rest_framework.response import Response
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('name', 'description', 'count', 'authors_of_the_book')




