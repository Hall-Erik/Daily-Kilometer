from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_auth.views import UserDetailsView
from .serializers import UserSerializer


class UserDetailView(UserDetailsView):
    serializer_class = UserSerializer


def profile(request, pk):
    owner = get_object_or_404(User, pk=pk)
    return render(request, 'users/profile.html', {'owner': owner})
