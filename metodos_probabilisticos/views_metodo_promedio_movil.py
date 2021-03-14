from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg
import io


from .forms import FormMuestra, FormValorMuestra
from .models import PromedioMovil

values = []
dfData = pd.DataFrame()

pm = PromedioMovil()

def promedio_movil(request):
    contexto = {"mensaje":"Estoy en promedio movil", "rango":range(10), 'titulo':'Promedio Móvil'}
    return render(request, "form_promedio_movil.html",contexto)


def form_valor_muestra(request):
    if request.method == "POST":
        formulario = FormMuestra(request.POST)
        if formulario.is_valid():
            datos = request.POST.dict()
            datos.pop('csrfmiddlewaretoken')
            cantidad_muestra = datos["muestra"]
            contexto = {"cantidad": range(int(cantidad_muestra)), 'titulo':'Promedio Móvil'}
            return render(request, "form_valor_muestra.html", contexto)
    return HttpResponseNotFound()


def form_dominio(request):
    if request.method == "POST":
        formulario = FormValorMuestra(request.POST)
        if formulario.is_valid():
            valores_muestra = request.POST.getlist("valor")

            for i,v in enumerate(valores_muestra):
                valores_muestra[i] = int(v)
            values = valores_muestra
            
            contexto = {'titulo':'Promedio Móvil'}
            return render(request, "form_dominio.html", contexto)
    return HttpResponseNotFound()


def promedio_movil2(request):
    if request.method == "POST":
        formulario = FormValorMuestra(request.POST)
        if formulario.is_valid():
            valores_muestra = request.POST.getlist("valor")

            for i,v in enumerate(valores_muestra):
                valores_muestra[i] = float(v)
            
            values = valores_muestra
            
            dfData = pd.DataFrame({'Valores':values})
            for i in range(0,dfData.shape[0]-2):
                dfData.loc[dfData.index[i+2],'Dominio 3'] = np.round(((dfData.iloc[i,0]+dfData.iloc[i+1,0]+dfData.iloc[i+2,0])/3),1)
    
            for i in range(0,dfData.shape[0]-3):
                dfData.loc[dfData.index[i+3],'Dominio 4'] = np.round(((dfData.iloc[i,0]+dfData.iloc[i+1,0]+dfData.iloc[i+2,0]+dfData.iloc[i+3,0])/4),1)
            min_valor = (len(dfData.index)-3)
            
            proyeccion = dfData.iloc[min_valor:,[0,1,2]]
            p1,p2,p3 =proyeccion.mean()
            
            a = dfData.append({'Valores':p1, 'Dominio 3':p2, 'Dominio 4':p3},ignore_index=True)
            a['Error Dominio 3'] = a['Valores']-a['Dominio 3']
            a['Error Dominio 4'] = a['Valores']-a['Dominio 4']

            pm.set_values(values)
            pm.set_mm3(list(a['Dominio 3']))
            pm.set_mm4(list(a['Dominio 4']))
            

            print(pm.get_values(), pm.get_mm3(), pm.get_mm4())

            dominio3 = list(a['Dominio 3'])

            
            
            contexto = {'data':a.to_html(classes="table table-striped table-hover text-dark"),'titulo':'Promedio Móvil','dominio3':dominio3}
            

            return render(request, 'promedio_movil.html', contexto)
    return HttpResponseNotFound()

def mostrar_grafico(request):
    a = {'Valores':pm.get_values(), 'Dominio 3':pm.get_mm3(), 'Dominio 4':pm.get_mm4()}
    print(request.GET.dict())
    f = plt.figure(figsize=[8,8])
    plt.grid(True)
    plt.plot(a['Valores'],label='Valores',marker='o')
    plt.plot(a['Dominio 3'],label='Media Móvil 3')
    plt.plot(a['Dominio 4'],label='Media Móvil 4')
    plt.legend(loc=2)

    buf = io.BytesIO()
    canvas = FigureCanvasAgg(f)
    canvas.print_png(buf)
    
    response = HttpResponse(buf.getvalue(), content_type='image/png')

    f.clear()
    response['Content-Length'] = str(len(response.content))

    return response
    #return HttpResponse()



