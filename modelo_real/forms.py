from django import forms
from .models import RLineaDeEspera



class RLineaEsperaFormCantidadMuestras(forms.ModelForm):
    class Meta:
        model = RLineaDeEspera
        fields = ['landa','nu']