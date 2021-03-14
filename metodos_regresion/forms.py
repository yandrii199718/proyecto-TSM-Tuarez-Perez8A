from django import forms
from .models import RegresionLineal
from .models import RegresionNoLineal

class RegresionLinealCantMuestrasForm(forms.Form):
    class Meta:
        model = RegresionLineal
        fields = ['cantidad']


class RegresionLinealMuestrasForm(forms.Form):
    class Meta:
        model = RegresionLineal
        fields = ['valor','x']

class RegresionNoLinealCantMuestrasForm(forms.Form):
    class Meta:
        model = RegresionNoLineal
        fields = ['cantidad']


class RegresionNoLinealMuestrasForm(forms.Form):
    class Meta:
        model = RegresionNoLineal
        fields = ['valor','x']

