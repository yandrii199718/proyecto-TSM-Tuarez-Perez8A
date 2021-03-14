from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render
from .forms import RLineaEsperaFormCantidadMuestras
from .models import RLineaDeEspera

import math, random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io
i = 0
# Create your views here.

ls = RLineaDeEspera()
def Rformulario_linea_espera(request):
    contexto = {'titulo':'Caso Real'}
    return render(request, 'form_real.html', contexto)
def Rperfil(request):
    contexto = {'titulo':'Perfil'}
    return render(request, 'perfil.html', contexto)    
def Rlinea_espera_resultado(request):
    if request.method == "POST":
        formulario = RLineaEsperaFormCantidadMuestras(request.POST)
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
            
            dfCalculos = pd.DataFrame({'Factor de utilización del sistema':[p], 'Probabilidad de que no haya unidades':[Po],'Longitud esperada en cola,':[Lq],'Número esperado de clientes en el sistema':[L],'Tiempo promedio que una unidad pasa en el sistema':[W],'Tiempo de espera en cola.':[Wq],'La probabilidad de que haya n unidades en el sistema':[Pn]})
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
            des = dfLE.describe()
            contexto = {'data':dfLE.to_html(classes="table table-striped table-hover text-dark"), 
            'descrip':des.to_html(classes="table table-striped table-hover text-dark"),
            'calculos':dfCalculos.to_html(classes="table table-striped table-hover text-dark"),
            'titulo':'Caso Real'}
            return render(request, 'real_resultado.html',contexto)
    else:
        return HttpResponseNotFound()

def Rls_grafica(request):
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