from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .forms import AditivoForm
from .models import Aditivo


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

import io

aditivo = Aditivo()

def metodo_aditivo(request):
    contexto = {"mensaje":"Estoy en aditivo", "rango":range(10),'titulo':'Congruencial Aditivo'}
    return render(request, 'form_aditivo.html',{'MENSAJE':'algo'})

def aditivo_resultado(request):
    if request.method == "POST":
        formulario = AditivoForm(request.POST)
        if formulario.is_valid():
            datos = request.POST.dict()
            datos.pop('csrfmiddlewaretoken')
            numero = int(datos['numero'])
            semilla = int(datos['semilla'])
            multiplicador = int(datos['multiplicador'])
            incremento = int(datos['incremento'])
            modulo = int(datos['modulo'])
            # Generador de números aleatorios Congruencia lineal
            x = [1] * numero
            r = [0.1] * numero
            for i in range(0, numero):
              x[i] = ((multiplicador*semilla)+incremento) % modulo
              semilla = x[i]
              r[i] = semilla / modulo
             # llenamos nuestro DataFrame
            d = {'Xn': x, 'ri': r }
            df = pd.DataFrame(data=d)
            
            aditivo.set_ri(list(df['ri']))
            contexto = {'data':df.to_html(classes="table table-striped table-hover text-dark"),'titulo':'Congruencial Aditivo'}
            return render(request, 'metodo_aditivo.html',contexto)
    else:
        return HttpResponseNotFound()


def aditivo_grafica(request):
    r = aditivo.get_ri()
    f = plt.figure(figsize=[8,8])
    plt.plot(r,marker='o')
    plt.title('Generador de Numeros Aleatorios Congruencial Aditivo')
    plt.xlabel('Serie')
    plt.ylabel('Aleatorios')

    buf = io.BytesIO()
    canvas = FigureCanvasAgg(f)
    canvas.print_png(buf)

    

    response = HttpResponse(buf.getvalue(), content_type='image/png')

    f.clear()
    response['Content-Length'] = str(len(response.content))
    
    return response