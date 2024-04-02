from django.shortcuts import render, redirect
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import *
from django.views.generic import ListView
from datetime import datetime
from .forms import *
import pytz

from .serializers import OrderSerializer

menu = [{'title': 'Home', 'url_name': 'home'},
        {'title': 'Users', 'url_name': 'users'},
        {'title': 'Orders', 'url_name': 'orders'},
        {'title': 'Books', 'url_name': 'books'},
        {'title': 'Authors', 'url_name': 'authors'}
        ]


class OrderHome(ListView):
    paginate_by = 9
    model = Order
    queryset = Order.objects.order_by('id')
    template_name = 'order/orders.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Orders'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['menu'] = menu
        return context



def show_oders_by_user(request, id_user):
    posts = Order.objects.filter(user_id=id_user)
    title = 'Orders'
    context = {
        "menu": menu,
        "title": title,
        "posts": posts,
    }
    return render(request, 'order/orders_by_user.html', context)


def show_order_by_id(request, id):
    post = Order.objects.get(id=id)
    title = f'Information about order № {post.id}'
    context = {
        "menu": menu,
        "title": title,
        "post": post,
    }
    return render(request, 'order/order_by_id.html', context)


def close_order(request, id):
    order = Order.objects.get(id=id)
    t = datetime.now()
    order.update(end_at=t)
    book = order.book
    book.count += 1
    book.save()
    return show_order_by_id(request, id)


def add_order(request, id_user):
    user = CustomUser.objects.get(id=id_user)
    if request.method == 'POST':
        form = AddOrderForm(request.POST)
        if form.is_valid():
            try:
                order = Order.create(user=user, **form.cleaned_data)
                return show_order_by_id(request, order.id)
            except:
                form.add_error(None, 'Error')
    else:
        form = AddOrderForm()
    title = 'Add order'
    context = {
        "menu": menu,
        "title": title,
        "form": form
    }
    return render(request, 'order/add_order.html', context)


def order_admin_filter(request):
    qs = Order.objects.all()
    id_query = request.GET.get('id')

    if id_query != "" and id_query is not None:
        qs = qs.filter(id=id_query)
    else:
        return redirect('orders')

    title = 'Orders'
    context = {
        "menu": menu,
        "title": title,
        "posts": qs,
    }
    return render(request, "order/orders.html", context)


def order_user_filter(request, id_user):
    qs = Order.objects.all()
    id_query = request.GET.get('id')

    if id_query != "" and id_query is not None:
        qs = qs.filter(id=id_query)
    else:
        show_oders_by_user(request, id_user)
    title = 'Orders'
    context = {
        "menu": menu,
        "title": title,
        "posts": qs,
    }
    return render(request, "order/orders_by_user.html", context)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)


class UserOrderList(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    lookup_field = 'user_id'
    permission_classes = (IsAdminUser,)


    def get_queryset(self):
        user_id = self.kwargs['user_id']
        order_id = self.kwargs.get('order_id', None)
        if order_id:
            filter = Order.objects.filter(user_id=user_id)
            return filter.filter(id=order_id)
        else:
            return Order.objects.filter(user_id=user_id)





# class OrderAPIView(generics.ListAPIView):
#     serializer_class = OrderSerializer
#     def get(self, request, *args, **kwargs):
#         id = kwargs.get('id', None)
#         user_id = kwargs.get('user_id', None)
#         order_id = kwargs.get('order_id', None)
#         if user_id and order_id:
#             order = Order.objects.filter(user_id=user_id, id=order_id)
#             return Response({'order': OrderSerializer(order, many=True).data})
#         elif user_id and not order_id:
#             orders = Order.objects.filter(user_id=user_id)
#         elif id:
#             order = Order.objects.filter(id=id)
#             return Response({'order': OrderSerializer(order, many=True).data})
#         else:
#             orders = Order.objects.all()
#         return Response({'orders': OrderSerializer(orders, many=True).data})
#
#     def post(self, request, *args, **kwargs):
#         user_id = kwargs.get('user_id', None)
#         if user_id:
#             request.data['user'] = user_id
#         serializer = OrderSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'order': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         id = kwargs.get('id', None)
#         order_id = kwargs.get('order_id', None)
#         user_id = kwargs.get('user_id', None)
#         if not id and not order_id:
#             return Response({'error': "Method put not allowed"})
#         try:
#             if id:
#                 instance = Order.objects.get(id=id)
#             elif order_id:
#                 filter = Order.objects.filter(user_id=user_id)
#                 instance = filter.get(id=order_id)
#         except:
#             return Response({'error': "Object does not exists"})
#         serializer = OrderSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'order': serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         id = kwargs.get('id', None)
#         order_id = kwargs.get('order_id', None)
#         user_id = kwargs.get('user_id', None)
#         if not id and not order_id:
#             return Response({'error': "Method DELETE not allowed"})
#         try:
#             if id:
#                 instance = Order.objects.get(id=id)
#             elif order_id:
#                 filter = Order.objects.filter(user_id=user_id)
#                 instance = filter.get(id=order_id)
#                 id = order_id
#             instance.delete()
#         except:
#             return Response({'error': "Object does not exists"})
#         return Response({'order': f'Order with id №{id} was removed'})

