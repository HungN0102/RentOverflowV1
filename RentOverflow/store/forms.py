from django import forms

class searchForm(forms.Form):
    location = forms.CharField(label='Location', max_length=255)