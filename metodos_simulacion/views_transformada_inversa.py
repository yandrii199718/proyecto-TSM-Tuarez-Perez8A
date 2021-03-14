from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from .forms import TransformadaForm
from .models import Transformada

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io

t = Transformada()

def transformada(request):
    if request.method == 'GET':
        contexto = {'titulo':'Transformada Inversa'}
        return render(request, 'transformada_inversa_landa.html', contexto)
    elif request.method == 'POST':
        formulario = TransformadaForm(request.POST)
        if formulario.is_valid():
            datos = request.POST.dict()
            datos.pop('csrfmiddlewaretoken')
            lambd = float(datos['lambd'])

            
            n, m, a, x0, c = 10, 2**32, 22695477, 4, 1
            x = [1] * n
            r = [0.1] * n
            for i in range(0, n):
                x[i] = ((a*x0)+c) % m
                x0 = x[i]
                r[i] = x0 / m
    
            d = {'Random': r }
            dfMCL = pd.DataFrame(data=d)
            dfexp = dfMCL['Random']
            exp_x = dfexp.values*(-1/lambd)*np.log(dfexp)
            dfMCL["Transformada"] = exp_x   

            t.set_df(dfMCL)

            contexto = {'titulo':'Transformada Inversa', 'data':dfMCL.to_html(classes="table table-striped table-hover text-dark")}
            return render(request, 'transformada_resultado.html', contexto)
    else:
        return HttpResponseNotFound()


def transformada_grafico(request):
    dfMCL = t.get_df()
    dfgrafico = dfMCL.filter(items=['Random','Transformada'])

    f = plt.figure(figsize=(50,15))
    plt.plot(dfgrafico)

    
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(f)
    canvas.print_png(buf)
    
    response = HttpResponse(buf.getvalue(), content_type='image/png')

    f.clear()
    response['Content-Length'] = str(len(response.content))

    return response