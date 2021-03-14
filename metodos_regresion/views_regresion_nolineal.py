from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .forms import RegresionNoLinealMuestrasForm, RegresionNoLinealCantMuestrasForm
from .models import RegresionNoLineal

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg
import io

regresion_lineal = RegresionNoLineal()


def regresion_nolineal_cant_muestra(request):
    contexto = {'titulo':'Regresión No Lineal'}
    return render(request, 'regresion_nolineal_cant_muestras.html', contexto)


def regresion_nolineal_muestras(request):
    if request.method == 'POST':
        formulario = RegresionNoLinealCantMuestrasForm(request.POST)
        if formulario.is_valid():
            datos = request.POST.dict()
            datos.pop('csrfmiddlewaretoken')
            cantidad = int(datos['cantidad'])

            contexto = {'cantidad':range(cantidad), 'titulo':'Regresión No Lineal'}
            return render(request, 'regresion_nolineal_muestras.html', contexto)
    else:
        return HttpResponseNotFound()


def regresion_nolineal_resultado(request):
    if request.method == 'POST':
        formulario = RegresionNoLinealMuestrasForm(request.POST)
        if formulario.is_valid():
            valores_muestra = request.POST.getlist("valor")
            x = request.POST.getlist("x")

            for i,v in enumerate(valores_muestra):
                valores_muestra[i] = float(v)
            for i,v in enumerate(x):
                x[i] = float(v)

            values = valores_muestra


            a = pd.DataFrame({'X':x,'Y':values})
            a['X^2'] = a['X']**2
            a['X^3'] = a['X']**3
            a['X^4'] = a['X']**4
            a['XY'] = a['X']*a['Y']
            a['X^2Y'] = (a['X']**2)*a['Y']
            
            y= a["Y"]
            
            p = np.polyfit(x,y,2)
            p0,p1,p2 = p
            
            regresion_lineal.set_valor(list(y))
            regresion_lineal.set_x(list(x))
            regresion_lineal.set_p(list(p))
            
            print ("El valor de p0 = ", p0, "Valor de p1 = ", p1, "Valor de p2 = ", p2)
            contexto ={'titulo':'Regresión No Lineal', 'p0':p0, 'p1':p1, 'p2':p2, 'data':a.to_html(classes="table table-striped table-hover text-dark")}
            
            return render(request, 'regresion_nolineal_resultado.html', contexto)
    else:
        return HttpResponseNotFound()

def regresion_nolineal_grafica(request):
    y = regresion_lineal.get_valor()
    x = np.array(regresion_lineal.get_x())
    p = regresion_lineal.get_p()

    y_ajuste = p[0]*x*x + p[1]*x + p[2]

    
    # dibujamos los datos experimentales de la recta
    f = plt.figure(figsize=[8,8])
    plt.plot(x,y,'b.')
    # Dibujamos la recta de ajuste
    plt.plot(x,y_ajuste, 'r-')
    plt.title('Ajuste Polimonial por mínimos cuadrados')
    plt.xlabel('Eje x')
    plt.ylabel('Eje y')
    plt.legend(('Datos experimentales','Ajustes Polimonial',), loc="upper left")
    

    buf = io.BytesIO()
    canvas = FigureCanvasAgg(f)
    canvas.print_png(buf)
    
    response = HttpResponse(buf.getvalue(), content_type='image/png')

    f.clear()
    response['Content-Length'] = str(len(response.content))

    return response