from django import forms
from .models import CuadradoMedio, Aditivo, Multiplicativo

class CuadradoMedioForm(forms.ModelForm):
    class Meta:
        model = CuadradoMedio
        fields = ['semilla','iteraciones']

class AditivoForm(forms.ModelForm):
    class Meta:
        model = Aditivo
        fields = ['semilla','multiplicador','incremento', 'modulo']


class MultiplicativoForm(forms.ModelForm):
    class Meta:
        model = Multiplicativo
        fields = ['moderna','semilla','incremento']

