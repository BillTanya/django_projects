from django.urls import path, include
from .views import *
from order.views import *
from book.views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'user', UserViewSet)

urlpatterns = [
    path('', home_page, name='home'),
    path('authentication/', UserHome.as_view(), name='users'),
    path('authentication/user/<int:id>/', show_user_by_id, name='user'),
    path('authentication/register/', RegisterUser.as_view(),  name='register'),
    path('authentication/login/', LoginUser.as_view(), name='login'),
    path('authentication/logout/', logout_user, name='logout'),
    path('api/v1/', include(router.urls)),
    # path('api/v1/user/', UserAPIList.as_view()),
    # path('api/v1/user/<int:pk>/', UserAPIDetailView.as_view())
]