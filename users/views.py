from django.shortcuts import render
from django.urls import reverse_lazy
from users.forms import (CustomUserCreationForm,
                         CustomUserChangeForm,
                         )
from django.views.generic import (CreateView, )
# Create your views here.


class RegisterUser(CreateView):
    template_name = 'users/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('core:movie_list')