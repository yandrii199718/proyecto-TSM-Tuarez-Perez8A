from django import forms
from .models import Montercarlo, Transformada

class MontecarloFormCantidadMuestras(forms.ModelForm):
    class Meta:
        model = Montercarlo
        fields = ['cantidad']

class MontecarloFormValorMuestra(forms.ModelForm):
    class Meta:
        model = Montercarlo
        fields = ['muestra']

class MontecarloFormCantidadEventos(forms.ModelForm):
    class Meta:
        model = Montercarlo
        fields = ['cantidad_eventos']

class TransformadaForm(forms.Form):
    class Meta:
        model = Transformada
        fields = ['lambd']