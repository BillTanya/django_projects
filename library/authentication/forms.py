from django.contrib.auth.forms import UserCreationForm, forms, AuthenticationForm
from .models import *


class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """
    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'middle_name', 'email')

    widgets = {
        'is_active': forms.BooleanField(),
    }



class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

