from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render
from .forms import LineasEsperaTiempoLlegadaMuestras, LineasEsperaTiempoServicioMuestras, LineasEsperaMontecarloIteraciones
from .models import LineaDeEsperaMontecarlo


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame

from pandas import DataFrame
import numpy as np
import math
import itertools
import random

lineas_montecarlo = LineaDeEsperaMontecarlo()


def cantidad_tiempo(request):
    if request.method == 'GET':
        contexto = {'titulo':'L.Espera Montecarlo'}
        return render(request, 'form_cantidad_llegada_montecarlo.html', contexto)
    elif request.method == 'POST':
        formulario = LineasEsperaTiempoLlegadaMuestras(request.POST)
        print(request.POST.getlist('tiempo_llegada'))
        if formulario.is_valid():
            muestras = request.POST.getlist('tiempo_llegada')
            for i,v in enumerate(muestras):
                muestras[i] = int(v)
            
            dfData = pd.DataFrame({'Tiempo entre llegadas':muestras})

            suma = dfData['Tiempo entre llegadas'].sum()            
            print('SumA',suma)
            n=len(dfData)

            x1 = dfData.assign(Probabilidad=lambda x: x['Tiempo entre llegadas'] / suma)
            a1 = np.cumsum(x1['Probabilidad'])
            x1['FPA'] = a1
            x1['Min'] = x1['FPA']
            x1['Max'] = x1['FPA']
            lis = x1["Min"].values
            lis2 = x1['Max'].values
            lis[0]= 0
            for i in range(1,len(x1)):
                lis[i] = lis2[i-1]

            x1['Min'] = lis

            max = x1['Max'].values
            min = x1['Min'].values
            print(x1)

            lineas_montecarlo.set_df_llegada(x1)
            
            contexto = {'titulo':'L.Espera Montecarlo'}
            return render(request, 'form_cantidad_servicio_montecarlo.html', contexto)
    else:
        return HttpResponseNotFound()


def cantidad_servicio(request):
    if request.method == 'POST':
        formulario = LineasEsperaTiempoServicioMuestras(request.POST)
        if formulario.is_valid():
            muestras = request.POST.getlist('tiempo_servicio')
            
            for i,v in enumerate(muestras):
                muestras[i] = int(v)

            dfData = pd.DataFrame({'Tiempo de servicio':muestras})

            suma = dfData['Tiempo de servicio'].sum()            
            n=len(dfData)

            x1 = dfData.assign(Probabilidad=lambda x: x['Tiempo de servicio'] / suma)
            a1 = np.cumsum(x1['Probabilidad'])
            x1['FPA'] = a1
            x1['Min'] = x1['FPA']
            x1['Max'] = x1['FPA']
            lis = x1["Min"].values
            lis2 = x1['Max'].values
            lis[0]= 0
            for i in range(1,len(x1)):
                lis[i] = lis2[i-1]

            x1['Min'] = lis

            max = x1['Max'].values
            min = x1['Min'].values

            print(x1)
            lineas_montecarlo.set_df_servicio(x1)
            
            contexto = {'titulo':'L.Espera Montecarlo'}
            return render(request, 'form_iteraciones_lineas_montecarlo.html', contexto)
    else:
        return HttpResponseNotFound()

def lineas_montecarlo_resultado(request):
    if request.method == 'POST':
        formulario = LineasEsperaMontecarloIteraciones(request.POST)
        if formulario.is_valid():
            muestras = request.POST.dict()
            numClientes = muestras['iteraciones']
            numClientes = int(numClientes)

            print('primer Punto')
            dfLlegada = lineas_montecarlo.get_df_llegada()
            dfServicio = lineas_montecarlo.get_df_servicio()
            n = len(dfLlegada)
            n1 = len(dfServicio)

            i = 0
            indice = ['ALL','ASE','TILL','TISE','TIRLL','TIISE','TIFSE','TIESP','TIESA']
            Clientes = np.arange(numClientes)
            dfLE = pd.DataFrame(index=Clientes, columns=indice).fillna(0.000)
            np.random.seed(100)

            max1 = dfLlegada['Max'].values
            min1 = dfLlegada['Min'].values

            max2 = dfServicio['Max'].values
            min2 = dfServicio['Min'].values

            posi = [0] * n
            posi2 = [0] * n1

            for i in Clientes:
                if i == 0:
                    
                    dfLE['ALL'][i] = random.random()
                    dfLE['ASE'][i] = random.random()   
                    for j in range(n):
                    
                        val = dfLE['ALL'][i]
                        pos = lineas_montecarlo.busqueda(min1,max1,val)
                        posi[j] = pos
                    for x in range(n):
                    
                        sim = dfLlegada.loc[dfLlegada.index == posi[x]]
                        simu = sim.filter(['Tiempo entre llegadas']).values
                        iterator = itertools.chain(*simu)
                        for item in iterator:
                            a=item
                            dfLE['TILL'][i] =round(a,2)

                    for j in range(n1):
                        val = dfLE['ASE'][i]
                        pos = lineas_montecarlo.busqueda(min2,max2,val)
                        posi2[j] = pos
                    for x in range(n1):
                        sim = dfServicio.loc[dfServicio.index == posi2[x]]
                        simu = sim.filter(['Tiempo de servicio']).values
                        iterator = itertools.chain(*simu)
                        for item in iterator:
                            a=item
                            dfLE['TISE'][i] = round(a,2)
                    dfLE['TIRLL'][i] = dfLE['TILL'][i]
                    dfLE['TIISE'][i] = dfLE['TIRLL'][i]
                    dfLE['TIFSE'][i] = dfLE['TIISE'][i] + dfLE['TISE'][i]
                    dfLE['TIESA'][i] = dfLE['TIESP'][i] + dfLE['TISE'][i]
                    print(dfLE)
                else:
                    dfLE['ALL'][i] = random.random()
                    dfLE['ASE'][i] = random.random()
                    for j in range(n):
                    
                        val = dfLE['ALL'][i]
                        pos = lineas_montecarlo.busqueda(min1,max1,val)
                        posi[j] = pos
                    for x in range(n):
                    
                        sim = dfLlegada.loc[dfLlegada.index == posi[x]]
                        simu = sim.filter(['Tiempo entre llegadas']).values
                        iterator = itertools.chain(*simu)
                        for item in iterator:
                            a=item
                            dfLE['TILL'][i] =round(a,2)

                    for j in range(n1):
                        val = dfLE['ASE'][i]
                        pos = lineas_montecarlo.busqueda(min2,max2,val)
                        posi2[j] = pos
                    for x in range(n1):
                        sim = dfServicio.loc[dfServicio.index == posi2[x]]
                        simu = sim.filter(['Tiempo de servicio']).values
                        iterator = itertools.chain(*simu)
                        for item in iterator:
                            a=item
                            dfLE['TISE'][i] = round(a,2)
                    dfLE['TIRLL'][i] = dfLE['TILL'][i] + dfLE['TIRLL'][i-1]
                    dfLE['TIISE'][i] = max(dfLE['TIRLL'][i],dfLE['TIFSE'][i-1])
                    dfLE['TIFSE'][i] = dfLE['TIISE'][i] + dfLE['TISE'][i]
                    dfLE['TIESP'][i] = dfLE['TIISE'][i] - dfLE['TIRLL'][i]
                    dfLE['TIESA'][i] = dfLE['TIESP'][i] + dfLE['TISE'][i]

            nuevas_columnas = pd.core.indexes.base.Index(["A_LLEGADA","A_SERVICIO","TIE_LLEGADA","TIE_SERVICIO","TIE_EXACTO_LLEGADA","TIE_INI_SERVICIO","TIE_FIN_SERVICIO","TIE_ESPERA","TIE_EN_SISTEMA"])
            dfLE.columns = nuevas_columnas
            
            contexto = {'titulo':'LE Montecarlo', 'llegada':dfLlegada.to_html(classes="table table-striped table-hover text-dark"), 
            'servicio':dfServicio.to_html(classes="table table-striped table-hover text-dark"),
            'data':dfLE.to_html(classes="table table-striped table-hover text-dark")}
            return render(request, 'linea_montecarlo_resultado.html', contexto)
    else:
        return HttpResponseNotFound()