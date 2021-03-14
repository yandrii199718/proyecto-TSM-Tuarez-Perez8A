from django import forms
from .models import MuestraAlisamiento, PromedioMovil

## Promedio movil
class FormMuestra(forms.ModelForm):
     class Meta:
        model = PromedioMovil
        fields = ['muestra']

class FormValorMuestra(forms.ModelForm):
     class Meta:
        model = PromedioMovil
        fields = ['valor']

class FormDominio(forms.ModelForm):
     class Meta:
        model = PromedioMovil
        fields = ['dominio']


##Alismiento exponencial
class FormMuestraAlisamiento(forms.ModelForm):
    class Meta:
        model = MuestraAlisamiento
        fields = ['muestra']

class FormValorMuestraAlisamiento(forms.ModelForm):
    class Meta:
        model = MuestraAlisamiento
        fields = ['valor']

class FormDominioAlisamiento(forms.ModelForm):
    class Meta:
        model = MuestraAlisamiento
        fields = ['dominio']
 