from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .forms import CuadradoMedioForm
from .models import CuadradoMedio


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

import io

cm = CuadradoMedio()

def cuadrado_medio(request):
    return render(request, 'form_cuadrado_medio.html',{'titulo':'Cuadrado Medio'})


def cuadrado_medio_resultado(request):
    if request.method == "POST":
        formulario = CuadradoMedioForm(request.POST)
        if formulario.is_valid():
            datos = request.POST.dict()
            datos.pop('csrfmiddlewaretoken')
            semilla = int(datos['semilla'])
            iteraciones = int(datos['iteraciones'])

            l=len(str(semilla)) 
            lista = [] 
            lista2 = []
            i=1
            while i < iteraciones:
                x=str(semilla*semilla) 
                if l % 2 == 0:
                    x = x.zfill(l*2)
                else:
                    x = x.zfill(l)
                y=(len(x)-l)/2
                y=int(y)
                semilla=int(x[y:y+l])
                lista.append(semilla)
                lista2.append(x)
                i=i+1
            df = pd.DataFrame({'X2':lista2,'Xi':lista})
            dfrac = df["Xi"]/10**l
            df["ri"] = dfrac

            cm.set_ri(list(df["ri"]))

            contexto = {'data':df.to_html(classes="table table-striped table-hover text-dark"), 'titulo':'Cuadrado Medio'}
            return render(request, 'cuadrado_medio.html',contexto)
    else:
        return HttpResponseNotFound()

def cuadrado_medio_grafica(request):
    ri = cm.get_ri()
    df = pd.DataFrame({'ri':ri})
    print(df['ri'])
    f = plt.figure(figsize=[8,8])
    plt.plot(df['ri'])
    plt.title('Generador de Numeros Aleatorios Cuadrados Medios')
    plt.xlabel('Serie')
    plt.ylabel('Aleatorios')

    buf = io.BytesIO()
    canvas = FigureCanvasAgg(f)
    canvas.print_png(buf)

    

    response = HttpResponse(buf.getvalue(), content_type='image/png')

    f.clear()
    response['Content-Length'] = str(len(response.content))
    
    return response