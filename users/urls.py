from django.urls import path
from users import views
from django.contrib.auth import views as auth_view
app_name = 'user'

urlpatterns = [
    path('login/', auth_view.LoginView.as_view(), name='login'),
    path('signup/', views.RegisterUser.as_view(), name='signup'),
    path('logout/', auth_view.LoginView.as_view(), name='logout'),
]