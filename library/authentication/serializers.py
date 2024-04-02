from datetime import datetime
from rest_framework import serializers
from rest_framework.response import Response
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'middle_name', 'last_name', 'email', 'created_at', 'updated_at')
