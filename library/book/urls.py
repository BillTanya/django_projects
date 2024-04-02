from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register(r'user', BookViewSet)

urlpatterns = [
    path('book/', BookHome.as_view(), name='books'),
    path('book/<int:id>/', show_book_by_id, name='book_id'),
    path('book/filter', book_filter, name='book_filter'),
    path('api/v1/', include(router.urls)),
]

