from django import forms
from .models import YourModel

class MyModelForm(forms.ModelForm):
    class Meta:
        model = YourModel
        fields = ['image']

