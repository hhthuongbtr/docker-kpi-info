from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from .models import Compare

class DateForm(forms.ModelForm):
    class Meta:
        model = Compare
        fields = ['date1', 'date2']
        widgets = {
            'date1': DatePickerInput(format='%Y-%m-%d').start_of('compare'),
            'date2': DatePickerInput(format='%Y-%m-%d').end_of('compare')
        }