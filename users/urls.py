from django.urls import path, include
from rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView)
from rest_auth.registration.views import RegisterView
from .views import profile, UserDetailView


app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserDetailView.as_view(), name='user_details'),
    path('password/change/', PasswordChangeView.as_view(),
         name='password_change'),
    path('password/reset/',
         include('django_rest_passwordreset.urls',
                 namespace='password_reset')),

    path('profile/<int:pk>/', profile, name='profile'),
]
