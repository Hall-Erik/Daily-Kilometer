from django import forms
from .models import Gear


class GearForm(forms.ModelForm):
    _DATE_INPUT_FORMATS = ['%m/%d/%Y']

    name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control gear-input'
        }))
    start_distance = forms.DecimalField(
        label='Starting Distance', required=False, initial=0.0,
        widget=forms.NumberInput(attrs={
            'placeholder': '0.0',
            'class': 'form-control dist-input'}))
    start_units = forms.ChoiceField(
        choices=(('mi', 'mi'), ('km', 'km')),
        widget=forms.Select(attrs={
            'class': 'form-control unit-input'}))
    date_added = forms.DateField(
        input_formats=_DATE_INPUT_FORMATS,
        widget=forms.DateInput(
            format='%m/%d/%Y',
            attrs={
                'id': 'datepicker',
                'autocomplete': 'off',
                'class': 'form-control date-input'}))

    class Meta:
        model = Gear
        fields = [
            'name',
            'start_distance',
            'start_units',
            'date_added',
        ]
