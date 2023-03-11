from django import forms
from django.core import validators


class AskForm(forms.Form):
    place = forms.CharField(validators=[
        validators.MinLengthValidator(2, "Please enter 2 or more characters")], required=True)
    duration = forms.IntegerField(validators=[validators.MinValueValidator(2, "Please plan for atleast 2 or more days")], required=True)

from django.forms import ModelForm
from .models import Queries

# Create the form class.
class QForm(ModelForm):
    class Meta:
        model = Queries
        fields = '__all__'
        widgets = {
            'place':forms.TextInput(attrs={'class':"form-control", 'placeholder':"Destination",'id':'place_id', 'type':'text'}),
            'duration':forms.NumberInput(attrs={'class':"form-control", 'placeholder':"No.of Days",'id':'duration_id', 'type':'number', 'onkeypress':"return (event.charCode !=8 && event.charCode ==0 || (event.charCode >= 48 && event.charCode <= 57))"}),
        }
