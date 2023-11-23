from django import forms
from .models import Sesion
class SesionForm(forms.ModelForm):
    class Meta:
        model = Sesion
        fields = '__all__'

    