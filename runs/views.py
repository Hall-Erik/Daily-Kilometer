from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from .models import Run
from .serializers import RunSerializer, RunCreateSerializer, GearSerializer
from .permissions import RunPermissions, GearPermissions


class RunPagination(PageNumberPagination):
    page_size = 10


class RunViewSet(ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer
    permission_classes = (RunPermissions,)
    lookup_field = 'id'
    pagination_class = RunPagination

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RunCreateSerializer
        return RunSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GearViewSet(ModelViewSet):
    serializer_class = GearSerializer
    permission_classes = (GearPermissions,)
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        return user.gear_set.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
