from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.views import generic
from django.utils import timezone
from .forms import CreateRunForm, CreateGearForm
from .models import Run, Gear


def index(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CreateRunForm(request.POST, user=request.user)
            if form.is_valid():
                data = form.cleaned_data
                run = Run(
                    date=data.get('date'),
                    distance=data.get('distance'),
                    units=data.get('units'),
                    duration=data.get('duration'),
                    user=request.user,
                    gear=data.get('gear'),
                )
                run.save()
                messages.success(request, 'Your run has been saved.')
                return redirect('runs:home')
            else:
                messages.error(
                    request, 'There was a problem. Please try again.')
        else:
            messages.warning(request, 'You need to log in to save runs.')
            return redirect('login')
    runs = Run.objects.order_by('-date')
    if request.user.is_authenticated:
        form = CreateRunForm(user=request.user)
    else:
        form = CreateRunForm(user=None)
    now = timezone.now().strftime('%m/%d/%Y')
    return render(
        request, 'runs/index.html',
        {
            'form': form,
            'now': now,
            'runs': runs}
    )


class DetailRunView(generic.DetailView):
    model = Run
    context_object_name = 'run'


class UpdateRunView(LoginRequiredMixin, UserPassesTestMixin,
                    SuccessMessageMixin, generic.UpdateView):
    model = Run
    context_object_name = 'run'
    form_class = CreateRunForm
    success_url = '/'
    success_message = 'Run updated'

    def get_form_kwargs(self):
        kwargs = super(UpdateRunView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def test_func(self):
        run = Run.objects.get(pk=self.kwargs.get('pk'))
        return run.user == self.request.user


class DeleteRunView(LoginRequiredMixin, UserPassesTestMixin,
                    generic.DeleteView):
    model = Run
    context_object_name = 'run'
    success_url = '/'

    def test_func(self):
        run = Run.objects.get(pk=self.kwargs.get('pk'))
        return run.user == self.request.user


class GearCreateView(LoginRequiredMixin, generic.CreateView):
    model = Gear
    context_object_name = 'shoe'
    form_class = CreateGearForm

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
    form_class = CreateGearForm

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
