from django import forms

class SubnetForm(forms.Form):
    address = forms.CharField(max_length=15)
    prefix = forms.IntegerField(max_value=30)
    