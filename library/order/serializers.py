from datetime import datetime
from rest_framework import serializers
from rest_framework.response import Response
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Order
        fields = ('id', 'book', 'user', 'created_at', 'plated_end_at', 'end_at')




