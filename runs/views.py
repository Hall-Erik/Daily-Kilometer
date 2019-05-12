from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.views import generic
from django.utils import timezone
from .forms import CreateRunForm
from .models import Run


def index(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CreateRunForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                run = Run(
                    date=data.get('date'),
                    distance=data.get('distance'),
                    units=data.get('units'),
                    duration=data.get('duration'),
                    user=request.user,
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
    form = CreateRunForm()
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


class UpdateRunView(SuccessMessageMixin, generic.UpdateView):
    model = Run
    context_object_name = 'run'
    form_class = CreateRunForm
    success_url = '/'
    success_message = 'Run updated'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = context['run'].date.strftime('%m/%d/%Y')
        return context


class DeleteRunView(generic.DeleteView):
    model = Run
    context_object_name = 'run'
    success_url = '/'
