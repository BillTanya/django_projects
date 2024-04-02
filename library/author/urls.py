from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register(r'user', AuthorViewSet)

urlpatterns = [
    path('author/', AuthorHome.as_view(), name='authors'),
    path('author/<int:id>/', show_author_by_id, name='author_by_id'),
    path('add-author/', add_author, name='add_author'),
    path('author/del/<int:id>/', delete_author_by_id, name='del_author_id'),
    path('api/v1/', include(router.urls)),
]