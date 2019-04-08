from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import CreateRunForm

runs = [
    {
        'date': timezone.now().strftime('%m/%d/%Y'),
        'distance': 2.5,
        'time': '10:15'
    },
    {
        'date': '03/03/2019',
        'distance': 3.1,
        'time': '31:15'
    },
    {
        'date': '01/22/2019',
        'distance': 4.5,
        'time': '40:55'
    },
]

def index(request):
    if request.method == 'POST':
        form = CreateRunForm(request.POST)
        if form.is_valid():
            distance = form.cleaned_data.get('distance')
            units = form.cleaned_data.get('units')
            print(distance, units)
            return redirect('runs-home')
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