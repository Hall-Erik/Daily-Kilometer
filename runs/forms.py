from django import forms
from .models import Run
from datetime import timedelta


class SplitDurationsWidget(forms.MultiWidget):
    '''
    Widget that splits duration into three number input boxes.
    '''
    def __init__(self, attrs={}):
        widgets = (
            forms.NumberInput(attrs={**attrs, **{'placeholder': 'hh'}}),
            forms.NumberInput(attrs={**attrs, **{'placeholder': 'mm'}}),
            forms.NumberInput(attrs={**attrs, **{'placeholder': 'ss'}}))
        super(SplitDurationsWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            hours = value.seconds // 3600
            minutes = (value.seconds % 3600) // 60
            seconds = value.seconds % 60
            return [int(hours), int(minutes), int(seconds)]
        return [None, None, None]


class MultiValueDurationField(forms.MultiValueField):
    widget = SplitDurationsWidget

    def __init__(self, *args, **kwargs):
        fields = (
            forms.IntegerField(),
            forms.IntegerField(),
            forms.IntegerField())
        super(MultiValueDurationField, self).__init__(
            fields=fields, require_all_fields=True, *args, **kwargs)

    def compress(self, data_list):
        if len(data_list) == 3:
            return timedelta(
                hours=int(data_list[0]) if data_list[0] else 0,
                minutes=int(data_list[1]) if data_list[1] else 0,
                seconds=int(data_list[2]) if data_list[2] else 0)
        else:
            return timedelta(0)


class CreateRunForm(forms.ModelForm):
    _DATE_INPUT_FORMATS = ['%m/%d/%Y']

    distance = forms.DecimalField(min_value=0.0)
    units = forms.ChoiceField(choices=(('mi', 'mi'), ('km', 'km')))
    duration = MultiValueDurationField(required=False)
    date = forms.DateField(
        input_formats=_DATE_INPUT_FORMATS,
        widget=forms.DateInput(format='%m/%d/%Y'))

    class Meta:
        model = Run
        fields = [
            'distance',
            'units',
            'duration',
            'date',
        ]

    def __init__(self, *args, **kwargs):
        super(CreateRunForm, self).__init__(*args, **kwargs)
