from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render
from .forms import MontecarloFormCantidadEventos, MontecarloFormCantidadMuestras, MontecarloFormValorMuestra
from .models import Montercarlo

import pandas as pd
import numpy as np
import itertools
import math
# Create your views here.

montecarlo = Montercarlo()

def formulario_montecarlo(request):
    contexto = {'titulo':'Montecarlo'}
    return render(request, 'montecarlo_cantidad_muestras.html', contexto)

def formulario_montecarlo_muestras(request):
    if request.method == 'POST':
        formulario = MontecarloFormCantidadMuestras(request.POST)
        if formulario.is_valid():
            datos = request.POST.dict()
            datos.pop('csrfmiddlewaretoken')
            cantidad = int(datos['cantidad'])

            contexto = {'titulo':'Montecarlo', 'cantidad':range(cantidad)}
            return render(request, 'montecarlo_muestras.html', contexto)
    else:
        return HttpResponseNotFound()

def formulario_montecarlo_eventos(request):
    if request.method == 'POST':
        formulario = MontecarloFormValorMuestra(request.POST)
        if formulario.is_valid():
            datos = request.POST.getlist('muestra')
            
            for i,v in enumerate(datos):
                datos[i] = float(v)
            
            montecarlo.set_muestras(datos)

            contexto = {'titulo':'Montecarlo'}

            return render(request, 'montecarlo_eventos.html', contexto)
    else:
        return HttpResponseNotFound()


def montecarlo_resultado(request):
    if request.method == 'POST':
        formulario = MontecarloFormCantidadEventos(request.POST)
        
        if formulario.is_valid():
            datos = request.POST.dict()
            cant_eventos = int(datos['cantidad_eventos'])

            n, m, a, x0, c = cant_eventos, 2**32, 22695477, 4, 1
            x = [1] * n
            r = [0.1] * n
            for i in range(0, n):
                x[i] = ((a*x0)+c) % m
                x0 = x[i]
                r[i] = x0 / m
    
            d = {'ri': r }
            dfRandom = pd.DataFrame(data=d)
            muestras = np.array(montecarlo.get_muestras())
            dfData = pd.DataFrame({'Valores':muestras})

            suma = dfData['Valores'].sum()            
            n=len(dfData)
            
            x1 = dfData.assign(Probabilidad=lambda x: x['Valores'] / suma)
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

            xpos = dfRandom['ri']
            posi = [0] * n
            for j in range(n):
                val = xpos[j]
                pos = montecarlo.busqueda(min,max,val)
                posi[j] = pos
                
            
            simula = []
            for j in range(n):
                for i in range(n):
                    sim = x1.loc[x1.index == posi[i]]
                    simu = sim.filter(['Valores']).values
                    iterator = itertools.chain(*simu)
                    for item in iterator:
                        a=item
                    simula.append(round(a,2))

            dfRandom["Simulación"] = pd.DataFrame(simula)   

            contexto ={'titulo':'Montecarlo', 'data':x1.to_html(classes="table table-striped table-hover text-dark"),
            'random':dfRandom.to_html(classes="table table-striped table-hover text-dark")}
            return render(request, 'montecarlo_resultado.html', contexto)
        return HttpResponse()
    
    return HttpResponseNotFound()


            
    