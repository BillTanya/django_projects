from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register(r'order', OrderViewSet)

urlpatterns = [
    path('order/', OrderHome.as_view(), name='orders'),
    path('order/<int:id>/', show_order_by_id, name='order_id'),
    path('order/close/<int:id>/', close_order, name='close_order'),
    path('order/add/<int:id_user>/', add_order, name='add_order'),
    path('orders/user/<int:id_user>/', show_oders_by_user, name='orders_by_user'),
    path('order/filter', order_admin_filter, name='order_admin_filter'),
    path('orders/user/<int:id_user>/filter', order_user_filter, name='order_user_filter'),
    path('api/v1/user/<int:user_id>/order/', UserOrderList.as_view()),
    path('api/v1/user/<int:user_id>/order/<int:order_id>/', UserOrderList.as_view()),
    path('api/v1/', include(router.urls)),

]