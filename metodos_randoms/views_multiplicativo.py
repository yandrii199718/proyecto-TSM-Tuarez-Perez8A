from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .forms import MultiplicativoForm
from .models import Multiplicativo


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

import io

multiplicativo = Multiplicativo()

def metodo_multiplicativo(request):
    return render(request, 'form_multiplicativo.html',{'titulo':'Congruencial  Multiplicativo'})

def multiplicativo_resultado(request):
    if request.method == "POST":
        formulario = MultiplicativoForm(request.POST)
        if formulario.is_valid():
            datos = request.POST.dict()
            datos.pop('csrfmiddlewaretoken')
            numero = int(datos['numero'])
            moderna = int(datos['moderna'])
            semilla = int(datos['semilla'])
            incremento = int(datos['incremento'])
    
            x = [1] * numero
            r = [0.1] * numero
 
            for i in range(0, numero):
              x[i] = (incremento*semilla) % moderna
              semilla = x[i]
              r[i] = semilla / moderna
            d = {'Xn': x, 'ri': r }
            df1 = pd.DataFrame(data=d)
            
            multiplicativo.set_ri(df1['ri'])

            contexto = {'data':df1.to_html(classes="table table-striped table-hover text-dark"), 'titulo':'Congruencial  Multiplicativo'}
            return render(request, 'metodo_multiplicativo.html',contexto)
    else:
        return HttpResponseNotFound()

def multiplicativo_grafica(request):
    r = multiplicativo.get_ri()
    f = plt.figure(figsize=[8,8])
    plt.plot(r,marker='o')
    plt.title('Generador de Numeros Aleatorios Congruencial Multiplicativo')
    plt.xlabel('Serie')
    plt.ylabel('Aleatorios')

    buf = io.BytesIO()
    canvas = FigureCanvasAgg(f)
    canvas.print_png(buf)

    

    response = HttpResponse(buf.getvalue(), content_type='image/png')

    f.clear()
    response['Content-Length'] = str(len(response.content))
    
    return response