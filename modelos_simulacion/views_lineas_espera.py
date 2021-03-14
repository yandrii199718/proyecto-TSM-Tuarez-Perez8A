from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render
from .forms import LineaEsperaFormCantidadMuestras
from .models import LineaDeEspera

import math, random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io
i = 0
# Create your views here.

ls = LineaDeEspera()
def formulario_linea_espera(request):
    contexto = {'titulo':'Lineas De Espera'}
    return render(request, 'form_linea.html', contexto)
def linea_espera_resultado(request):
    if request.method == "POST":
        formulario = LineaEsperaFormCantidadMuestras(request.POST)
        if formulario.is_valid():
            datos = request.POST.dict()
            datos.pop('csrfmiddlewaretoken')
            numClientes = int(datos['numero'])
            landa = float(datos['landa'])
            nu = float(datos['nu'])
            
            p=landa/nu
            Po = 1.0 - (landa/nu)
            Lq = landa*landa / (nu * (nu - landa))
            L = landa /(nu - landa)
            W = 1 / (nu - landa)
            Wq = W - (1.0 / nu)
            n = 1
            Pn = (landa/nu)*n*Po
            
            dfCalculos = pd.DataFrame({'P':[p], 'Po':[Po],'Lq':[Lq],'L':[L],'W':[W],'Wq':[Wq],'Pn':[Pn]})
            print(dfCalculos)
            numClientes = int(datos['numero'])
            i = 0
            indice = ['ALL','ASE','TILL','TISE','TIRLL','TIISE','TIFSE','TIESP','TIESA']
            Clientes = np.arange(numClientes)
            dfLE = pd.DataFrame(index=Clientes, columns=indice).fillna(0.000)
            np.random.seed(100)
            for i in Clientes:
                if i == 0:
                    dfLE['ALL'][i] = random.random()
                    dfLE['ASE'][i] = random.random()
                    dfLE['TILL'][i] = -landa*np.log(dfLE['ALL'][i])
                    dfLE['TISE'][i] = -nu*np.log(dfLE['ASE'][i])
                    dfLE['TIRLL'][i] = dfLE['TILL'][i]
                    dfLE['TIISE'][i] = dfLE['TIRLL'][i]
                    dfLE['TIFSE'][i] = dfLE['TIISE'][i] + dfLE['TISE'][i]
                    dfLE['TIESA'][i] = dfLE['TIESP'][i] + dfLE['TISE'][i]
                else:
                    dfLE['ALL'][i] = random.random()
                    dfLE['ASE'][i] = random.random()
                    dfLE['TILL'][i] = -landa*np.log(dfLE['ALL'][i])
                    dfLE['TISE'][i] = -nu*np.log(dfLE['ASE'][i])
                    dfLE['TIRLL'][i] = dfLE['TILL'][i] + dfLE['TIRLL'][i-1]
                    dfLE['TIISE'][i] = max(dfLE['TIRLL'][i],dfLE['TIFSE'][i-1])
                    dfLE['TIFSE'][i] = dfLE['TIISE'][i] + dfLE['TISE'][i]
                    dfLE['TIESP'][i] = dfLE['TIISE'][i] - dfLE['TIRLL'][i]
                    dfLE['TIESA'][i] = dfLE['TIESP'][i] + dfLE['TISE'][i]
                    
            nuevas_columnas = pd.core.indexes.base.Index(["A_LLEGADA","A_SERVICIO","TIE_LLEGADA","TIE_SERVICIO","TIE_EXACTO_LLEGADA","TIE_INI_SERVICIO","TIE_FIN_SERVICIO","TIE_ESPERA","TIE_EN_SISTEMA"])
            dfLE.columns = nuevas_columnas

            ls.set_df(dfLE)
            contexto = {'data':dfLE.to_html(classes="table table-striped table-hover text-dark"), 
            'calculos':dfCalculos.to_html(classes="table table-striped table-hover text-dark"),
            'titulo':'Lineas De Espera'}
            return render(request, 'linea_resultado.html',contexto)
    else:
        return HttpResponseNotFound()

def ls_grafica(request):
    df = ls.get_df()
    f = plt.figure()
    plt.plot(df)
    plt.legend(df.columns, loc="upper left")

    
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(f)
    canvas.print_png(buf)
    
    response = HttpResponse(buf.getvalue(), content_type='image/png')

    f.clear()
    response['Content-Length'] = str(len(response.content))

    return response
