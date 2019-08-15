from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.views import generic
from django.utils import timezone
from .forms import GearForm
from .models import Run, Gear
from rest_framework.viewsets import ModelViewSet
from .serializers import RunSerializer
from .permissions import IsOwnerCanPostOrReadOnly


class RunViewSet(ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer
    permission_classes = (IsOwnerCanPostOrReadOnly,)
    lookup_field = 'id'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GearCreateView(LoginRequiredMixin, generic.CreateView):
    model = Gear
    context_object_name = 'shoe'
    form_class = GearForm

    def get_context_data(self, **kwargs):
        context = super(GearCreateView, self).get_context_data(**kwargs)
        context['now'] = timezone.now().strftime('%m/%d/%Y')
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(GearCreateView, self).form_valid(form)


class GearListView(LoginRequiredMixin, generic.ListView):
    model = Gear
    context_object_name = 'shoes'

    def get_queryset(self):
        return self.request.user.gear_set.order_by('-date_added')


class GearDetailView(generic.DetailView):
    model = Gear
    context_object_name = 'shoe'


class GearUpdateView(LoginRequiredMixin, UserPassesTestMixin,
                     generic.UpdateView):
    model = Gear
    context_object_name = 'shoe'
    form_class = GearForm

    def test_func(self):
        gear = Gear.objects.get(pk=self.kwargs.get('pk'))
        return gear.owner == self.request.user


class GearDeleteView(LoginRequiredMixin, UserPassesTestMixin,
                     generic.DeleteView):
    model = Gear
    context_object_name = 'shoe'
    success_url = '/'

    def test_func(self):
        gear = Gear.objects.get(pk=self.kwargs.get('pk'))
        return gear.owner == self.request.user
