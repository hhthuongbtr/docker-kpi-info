from django import forms
from bootstrap_datepicker_plus import DatePickerInput

class DateForm(forms.Form):
    date = forms.DateField(
        widget = DatePickerInput(format='%Y-%m-%d')
    )