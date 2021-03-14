from django import forms
from .models import LineaDeEspera, ModeloInventario, LineaDeEsperaMontecarlo


class LineaEsperaFormCantidadMuestras(forms.ModelForm):
    class Meta:
        model = LineaDeEspera
        fields = ['landa','nu']

class InventarioFormCantidadMuestras(forms.ModelForm):
    class Meta:
        model = ModeloInventario
        fields = ['demanda','costoO','costoM','costoP','Tespera','DiasAno']

class LineasEsperaTiempoLlegadaMuestras(forms.ModelForm):
    class Meta:
        model = LineaDeEsperaMontecarlo
        fields = ['cant_tiempo', 'tiempo_llegada']

class LineasEsperaTiempoServicioMuestras(forms.ModelForm):
    class Meta:
        model = LineaDeEsperaMontecarlo
        fields = ['cant_servicio', 'tiempo_servicio']

class LineasEsperaMontecarloIteraciones(forms.ModelForm):
    class Meta:
        model = LineaDeEsperaMontecarlo
        fields = ['iteraciones']