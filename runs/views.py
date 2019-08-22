from rest_framework.viewsets import ModelViewSet
from .models import Run, Gear
from .serializers import RunSerializer, RunCreateSerializer, GearSerializer
from .permissions import RunPermissions, GearPermissions


class RunViewSet(ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer
    permission_classes = (RunPermissions,)
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RunCreateSerializer
        return RunSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GearViewSet(ModelViewSet):
    queryset = Gear.objects.all()
    serializer_class = GearSerializer
    permission_classes = (GearPermissions,)
    lookup_field = 'id'

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
