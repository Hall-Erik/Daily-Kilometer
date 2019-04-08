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
        self.fields['distance'].widget.attrs.update({'width': 500})
        self.fields['date'].widget.attrs.update(
            {'id': 'datepicker', 'width': 276})
        self.fields['date'].input_formats=['%d/%m/%Y']
        self.fields['hours'].widget.attrs.update(
            {'value': '00'})