from django.contrib import messages
from django.shortcuts import render, redirect
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
                    hours=data.get('hours'),
                    minutes=data.get('minutes'),
                    seconds=data.get('seconds'),
                    user=request.user,
                )
                run.save()
                messages.success(request, 'Your run has been saved.')
                return redirect('runs-home')
            else: 
                messages.error(request, 'There was a problem. Please try again.')
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
             'runs': runs
        }
    )