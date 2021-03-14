from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

import io

from .forms import FormMuestraAlisamiento, FormValorMuestraAlisamiento, FormDominioAlisamiento
from .models import MuestraAlisamiento

values = []
dfData = pd.DataFrame()
alisamiento =  MuestraAlisamiento()

def alisamiento_exponencial(request):
    contexto = {"mensaje":"Estoy en alisamiento", "rango":range(10), 'titulo':'Alisamiento Exponencial'}
    return render(request, "form_alisamiento.html",contexto)


def form_alisamiento_muestra(request):
    if request.method == "POST":
        formulario = FormMuestraAlisamiento(request.POST)
        if formulario.is_valid():
            datos = request.POST.dict()
            datos.pop('csrfmiddlewaretoken')
            cantidad_muestra = datos["muestra"]
            contexto = {"cantidad": range(int(cantidad_muestra)), 'titulo':'Alisamiento Exponencial'}
            return render(request, "form_muestra_alisamiento.html", contexto)
    return HttpResponseNotFound()


def form_alisamiento_dominio(request):
    if request.method == "POST":
        formulario = FormValorMuestraAlisamiento(request.POST)
        if formulario.is_valid():
            valores_muestra = request.POST.getlist("valor")

            for i,v in enumerate(valores_muestra):
                valores_muestra[i] = float(v)
            values = valores_muestra
            
            alisamiento.set_values(values)
            print(alisamiento.get_values())

            contexto = {'titulo':'Alisamiento Exponencial'}
            return render(request, "form_alfa_alisamiento.html", contexto)
    return HttpResponseNotFound()


def alisamiento_resultado(request):
    if request.method == "POST":
        formulario = FormDominioAlisamiento(request.POST)
        if formulario.is_valid():
            
            alfa = request.POST.dict()
            alfa.pop('csrfmiddlewaretoken')
            alfa = float(alfa["dominio"])
            unoalfa = 1 - alfa

            
            values = alisamiento.get_values()
            dfData = pd.DataFrame({'Valores':values})
            
            for i in range(0,dfData.shape[0]-1):
                dfData.loc[dfData.index[i+1],'SN'] = np.round(dfData.iloc[i,0],1)
            
            for i in range(2,dfData.shape[0]):
                dfData.loc[dfData.index[i],'SN'] = np.round(dfData.iloc[i-1,0],1)*alfa + np.round(dfData.iloc[i-1,1],1)*unoalfa
            i=i+1
            p1=0
            p2=np.round(dfData.iloc[i-1,0],1)*alfa + np.round(dfData.iloc[i-1,1],1)*unoalfa
            a = dfData.append({'Valores':p1, 'SN':p2},ignore_index=True)
            
            alisamiento.set_suavizacion(list(a['SN']))

            contexto = {'data':a.to_html(classes="table table-striped table-hover text-dark"),'titulo':'Alisamiento Exponencial'}
            return render(request, 'alisamiento_exponencial.html', contexto)

    return HttpResponseNotFound()


def alisamiento_grafica(request):
    values = alisamiento.get_values()
    suavizacion = alisamiento.get_suavizacion()

    df = pd.DataFrame({'Valores':values})

    print(values, "Suavizacion")
    f = plt.figure(figsize=[8,8])
    plt.grid(True)
    plt.plot(df['Valores'],label='Valores',marker='o')
    plt.legend(loc=2)

    buf = io.BytesIO()
    canvas = FigureCanvasAgg(f)
    canvas.print_png(buf)

    

    response = HttpResponse(buf.getvalue(), content_type='image/png')

    f.clear()
    response['Content-Length'] = str(len(response.content))
    
    return response