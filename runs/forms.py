from django import forms

class CreateRunForm(forms.Form):
    distance = forms.DecimalField()
    units = forms.ChoiceField(choices=(('mi', 'mi'), ('km', 'km')))
    hours = forms.IntegerField()
    minutes = forms.IntegerField(max_value=59)
    seconds = forms.IntegerField(max_value=59)
    date = forms.DateField()

    def __init__(self, *args, **kwargs):
        super(CreateRunForm, self).__init__(*args, **kwargs)
        self.fields['distance'].widget.attrs.update(
            {'value': '00', 'width': 500})
        # self.fields['units'].widget.attrs.update({})
        self.fields['date'].widget.attrs.update(
            {'id': 'datepicker', 'width': '200px'})
        self.fields['date'].input_formats=['%d/%m/%Y']
        self.fields['hours'].widget.attrs.update(
            {'value': '00', 'class': 'time-input'})
        self.fields['minutes'].widget.attrs.update(
            {'value': '00', 'class': 'time-input'})
        self.fields['seconds'].widget.attrs.update(
            {'value': '00', 'class': 'time-input'})