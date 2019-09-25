from django import forms

class DateRangeForm(forms.Form):
    start_date = forms.DateField(input_formats=[ '%Y-%m-%d' ], required=True)
    end_date = forms.DateField(input_formats=[ '%Y-%m-%d' ], required=True)

class ServerDateRangeForm(forms.Form):
    server_index = forms.CharField(max_length=20)
    start_date = forms.DateField(input_formats=[ '%Y-%m-%d' ], required=True)
    end_date = forms.DateField(input_formats=[ '%Y-%m-%d' ], required=True)