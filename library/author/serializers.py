from datetime import datetime
from rest_framework import serializers
from rest_framework.response import Response
from .models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('name', 'surname', 'patronymic', 'authors_books')




