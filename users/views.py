from rest_auth.views import UserDetailsView
from .serializers import UserSerializer


class UserDetailView(UserDetailsView):
    serializer_class = UserSerializer
