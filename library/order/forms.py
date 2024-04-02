from django import forms
from .models import *
from datetime import datetime
from authentication.models import *
from book.models import *
from datetime import datetime, timedelta

DATETIME = datetime.now() + timedelta(days=14)

class AddOrderForm(forms.Form):
    # user = forms.ModelChoiceField(queryset=CustomUser.objects.filter(role=0), label="User")
    book = forms.ModelChoiceField(queryset=Book.objects.all(), label="Book")
    plated_end_at = forms.DateTimeField(label="Plated end at", initial=DATETIME)


    # book = models.ForeignKey(Book, on_delete=models.CASCADE, default=None)
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    # created_at = models.DateTimeField(auto_now_add=True)
    # end_at = models.DateTimeField(default=None, null=True, blank=True)
    # plated_end_at = models.DateTimeField(default=None)


    # class Meta:
    #     model = Order
    #     fields = ['user', 'book', 'plated_end_at']
        # widgets = {
        #     'user': forms.ModelChoiceField(queryset=CustomUser.objects.filter(role=0), label="user", to_field_name='users')
        # }