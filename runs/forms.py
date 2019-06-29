from django import forms
from .models import Run, Gear
from datetime import timedelta


class SplitDurationsWidget(forms.MultiWidget):
    '''
    Widget that splits duration into three number input boxes.
    '''
    def __init__(self, attrs={}):
        widgets = (
            forms.NumberInput(attrs={
                **attrs, **{
                    'placeholder': 'hh',
                    'class': 'form-control time-input'}}),
            forms.NumberInput(attrs={
                **attrs, **{
                    'placeholder': 'mm',
                    'class': 'form-control time-input'}}),
            forms.NumberInput(attrs={
                **attrs, **{
                    'placeholder': 'ss',
                    'class': 'form-control time-input'}}))
        super(SplitDurationsWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            hours = value.seconds // 3600
            minutes = (value.seconds % 3600) // 60
            seconds = value.seconds % 60
            return [int(hours), int(minutes), int(seconds)]
        return [None, None, None]


class MultiValueDurationField(forms.MultiValueField):
    '''
    Duration field broken into three inputs: hours, minutes, seconds
    '''
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


class RunForm(forms.ModelForm):
    _DATE_INPUT_FORMATS = ['%m/%d/%Y']
    _run_choices = (
        ('', '----------'),
        ('Road run', 'Road run'),
        ('Trail run', 'Trail run'),
        ('Race', 'Race'),
        ('Treadmill', 'Treadmill'))

    distance = forms.DecimalField(
        min_value=0.0,
        widget=forms.NumberInput(attrs={
            'placeholder': '0.0',
            'class': 'form-control dist-input'}))
    units = forms.ChoiceField(
        choices=(('mi', 'mi'), ('km', 'km')),
        widget=forms.Select(attrs={
            'class': 'form-control unit-input'}))
    duration = MultiValueDurationField(required=False)
    date = forms.DateField(
        input_formats=_DATE_INPUT_FORMATS,
        widget=forms.DateInput(
            format='%m/%d/%Y',
            attrs={
                'id': 'datepicker',
                'autocomplete': 'off',
                'class': 'form-control date-input'}))
    gear = forms.ModelChoiceField(
        None,
        widget=forms.Select(attrs={'class': 'form-control gear-input'}),
        required=False)
    description = forms.CharField(
        max_length=240, required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'}))
    run_type = forms.ChoiceField(
        choices=_run_choices,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control gear-input'}))

    class Meta:
        model = Run
        fields = [
            'distance',
            'units',
            'duration',
            'date',
            'gear',
            'description',
            'run_type',
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(RunForm, self).__init__(*args, **kwargs)
        gear = Gear.objects.filter(owner=user).order_by('-date_added')
        self.fields['gear'].queryset = gear
        if gear:
            self.fields['gear'].initial = gear.first().id


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
