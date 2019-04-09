from django import forms
from .models import Run

class CreateRunForm(forms.ModelForm):
    _DATE_INPUT_FORMATS = ['%m/%d/%Y']

    distance = forms.DecimalField(min_value=0.0)
    units = forms.ChoiceField(choices=(('mi', 'mi'), ('km', 'km')))
    hours = forms.IntegerField(min_value=0)
    minutes = forms.IntegerField(max_value=59, min_value=0)
    seconds = forms.IntegerField(max_value=59, min_value=0)
    date = forms.DateField(input_formats=_DATE_INPUT_FORMATS)

    class Meta:
        model = Run
        fields = [
            'distance',
            'units',
            'hours',
            'minutes',
            'seconds',
            'date',
        ]

    def __init__(self, *args, **kwargs):
        super(CreateRunForm, self).__init__(*args, **kwargs)