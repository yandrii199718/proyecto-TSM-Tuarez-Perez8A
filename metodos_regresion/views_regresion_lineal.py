from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .forms import RegresionLinealMuestrasForm, RegresionLinealCantMuestrasForm
from .models import RegresionLineal

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg
import io

regresion_lineal = RegresionLineal()


def regresion_lineal_cant_muestra(request):
    contexto = {'Mensaje':'En regresion lineal', 'title':'Regresión Lineal'}
    return render(request, 'regresion_lineal_cant_muestra.html', contexto)


def regresion_lineal_muestras(request):
    if request.method == 'POST':
        formulario = RegresionLinealCantMuestrasForm(request.POST)
        if formulario.is_valid():
            datos = request.POST.dict()
            datos.pop('csrfmiddlewaretoken')
            cantidad = int(datos['cantidad'])

            contexto = {'cantidad':range(cantidad), 'title':'Regresión Lineal'}
            return render(request, 'regresion_lineal_muestras.html', contexto)
    else:
        return HttpResponseNotFound()


def regresion_lineal_resultado(request):
    if request.method == 'POST':
        formulario = RegresionLinealMuestrasForm(request.POST)
        if formulario.is_valid():
            valores_muestra = request.POST.getlist("valor")
            x = request.POST.getlist("x")
            for i,v in enumerate(valores_muestra):
                valores_muestra[i] = float(v)

            for i, v in enumerate(x):
                x[i] = float(v)
            
            values = valores_muestra


            a = pd.DataFrame({'X':x, 'Y':values})
            a['X^2'] = a['X']**2
            a['XY'] = a['X']*a['Y']
            a['Y^2'] = a['Y']**2
            x = a['X']
            y= a["Y"]
            
            p = np.polyfit(x,y,1)
            p0,p1 = p
            
            regresion_lineal.set_valor(list(y))
            regresion_lineal.set_x(list(x))
            regresion_lineal.set_p(list(p))
            
            print ("El valor de p0 = ", p0, "Valor de p1 = ", p1)
            contexto ={'title':'Regresión Lineal', 'p0':p0, 'p1':p1, 'data':a.to_html(classes="table table-striped table-hover text-dark")}
            
            return render(request, 'regresion_lineal_resultado.html', contexto)
    else:
        return HttpResponseNotFound()

def regresion_lineal_grafica(request):
    y = regresion_lineal.get_valor()
    x = np.array(regresion_lineal.get_x())
    p = regresion_lineal.get_p()

    y_ajuste = p[0]*x + p[1]
    
    # dibujamos los datos experimentales de la recta
    f = plt.figure()
    plt.plot(x,y,'b.')
    # Dibujamos la recta de ajuste
    plt.plot(x,y_ajuste, 'r-')
    plt.title('Ajuste lineal por mínimos cuadrados')
    plt.xlabel('Eje x')
    plt.ylabel('Eje y')
    plt.legend(('Datos experimentales','Ajuste lineal',), loc="upper left")
    

    buf = io.BytesIO()
    canvas = FigureCanvasAgg(f)
    canvas.print_png(buf)
    
    response = HttpResponse(buf.getvalue(), content_type='image/png')

    f.clear()
    response['Content-Length'] = str(len(response.content))

    return response