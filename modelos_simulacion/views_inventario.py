from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render
from .forms import InventarioFormCantidadMuestras
from .models import ModeloInventario

from math import sqrt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io
from pandas import DataFrame
import numpy as np

mi = ModeloInventario()


make_distribution : int 
def formulario_inventario(request):
    contexto = {'titulo':'Modelo Inventario'}
    return render(request, 'form_inventario.html', contexto)
def m_inventario_resultado(request):
    if request.method == "POST":
        formulario = InventarioFormCantidadMuestras(request.POST)
        if formulario.is_valid():
            datos = request.POST.dict()
            datos.pop('csrfmiddlewaretoken')
            k = int(datos['numero'])
            demand = float(datos['demanda'])
            Co = float(datos['costoO'])
            Ch = float(datos['costoM'])
            P = float(datos['costoP'])
            lead_time = float(datos['Tespera'])
            DiasAno = float(datos['DiasAno'])
            Q = round(sqrt(((2*Co*demand)/Ch)),2)
            N = round(demand / Q,2)
            R = round((demand / DiasAno) * lead_time,2)
            T = round(DiasAno / N,2)
            CoT = N * Co
            ChT = round(Q / 2 * Ch,2)
            MOQ = round(CoT + ChT,2)
            CTT = round(P * demand + MOQ,2)
            dfCalculos = pd.DataFrame({'Cant Optima':[Q], 'N° de pedidos':[N],'P. de reorden':[R],'T. entre pedido':[T],'C. total de Ordenar':[CoT],' C. Mantener Inventario':[ChT],'C. Total de Ordenar y Mantener Inventario':[MOQ],'C. Total del Sistema de Inventario':[CTT]})
            
            indice = ['Q','Costo_ordenar','Costo_Mantenimiento','Costo_total','Diferencia_Costo_Total']

            periodo = np.arange(k)

            def genera_lista(Q):
                k = int(datos['numero'])
                Q_Lista = []
                i = 1
                Qi = Q
                Q_Lista.append(Qi)
                for i in range(1,9):
                      Qi = Qi - 60
                      Q_Lista.append(Qi)

                Qi = Q
                for i in range(9, k):
                     Qi = Qi + 60
                     Q_Lista.append(Qi)
                return Q_Lista
            Lista= genera_lista(Q)
            Lista.sort()
            dfQ = DataFrame(index=periodo, columns=indice).fillna(0)
            dfQ['Q'] = Lista
            #dfQ
            for period in periodo:
                dfQ['Costo_ordenar'][period] = demand * Co / dfQ['Q'][period]
                dfQ['Costo_Mantenimiento'][period] = dfQ['Q'][period] * Ch / 2
                dfQ['Costo_total'][period] = dfQ['Costo_ordenar'][period] + dfQ['Costo_Mantenimiento'][period]
                dfQ['Diferencia_Costo_Total'][period] = dfQ['Costo_total'][period] - MOQ
            
            mi.set_df(dfQ) 

            def make_data(product, policy, periods):
                periods += 1
                # Create zero-filled Dataframe
                period_lst = np.arange(periods) # index
                header = ['INV_INICIAL','INV_NETO_INICIAL','DEMANDA', 'INV_FINAL','INV_FINAL_NETO', 'VENTAS_PERDIDAS', 'INV_PROMEDIO', 'CANT_ORDENAR', 'TIEMPO_LLEGADA']
                df = DataFrame(index=period_lst, columns=header).fillna(0)
                # Create a list that will store each period order
                order_l = [Order(quantity=0, lead_time=0)
                        for x in range(periods)]
                                # Fill DataFrame
                for period in period_lst:
                    if period == 0:
                        df['INV_INICIAL'][period] = product.initial_inventory 
                        df['INV_NETO_INICIAL'][period] = product.initial_inventory
                        df['INV_FINAL'][period] = product.initial_inventory
                        df['INV_FINAL_NETO'][period] = product.initial_inventory
                    if period >= 1:
                        df['INV_INICIAL'][period] = df['INV_FINAL'][period - 1] + order_l[period - 1].quantity
                        df['INV_NETO_INICIAL'][period] = df['INV_FINAL_NETO'][period - 1] + pending_order(order_l, period)
                        #demand = int(product.demand())
                        demand = float(datos['demanda'])
                        # We can't have negative demand
                        if demand > 0:
                            df['DEMANDA'][period] = demand
                        else:
                            df['DEMANDA'][period] = 0
                        # We can't have negative INV_INICIAL
                        if df['INV_INICIAL'][period] - df['DEMANDA'][period] < 0:
                            df['INV_FINAL'][period] = 0
                        else:
                            df['INV_FINAL'][period] = df['INV_INICIAL'][period] - df['DEMANDA'][period]
                        order_l[period].quantity, order_l[period].lead_time = placeorder(product, df['INV_FINAL'][period], policy,period)
                        df['INV_FINAL_NETO'][period] = df['INV_NETO_INICIAL'][period] - df['DEMANDA'][period]
                        if df['INV_FINAL_NETO'][period] < 0:
                            df['VENTAS_PERDIDAS'][period] = abs(df['INV_FINAL_NETO'][period])
                            df['INV_FINAL_NETO'][period] = 0
                        else:
                            df['VENTAS_PERDIDAS'][period] = 0
                        df['INV_PROMEDIO'][period] = (df['INV_NETO_INICIAL'][period] + df['INV_FINAL_NETO'][period]) / 2.0
                        df['CANT_ORDENAR'][period] = order_l[period].quantity
                        df['TIEMPO_LLEGADA'][period] = order_l[period].lead_time
                return df           
            def pending_order(order_l, period):
                """Return the order that arrives in actual period"""
                indices = [i for i, order in enumerate(order_l) if order.quantity]
                sum = 0
                for i in indices:
                    if period-(i+ order_l[i].lead_time+1) ==0:
                        sum += order_l[i].quantity
                return sum
            def demanda(self):
                    if self.demand_dist == "Constant":
                        return self.demand_p1
                    elif self.demand_dist == "Normal":
                        return make_distribution(
                            np.random.normal,
                            self.demand_p1,
                            self.demand_p2)()
                    elif self.demand_dist == "Triangular":
                        return make_distribution(
                            np.random_triangular,
                            self.demand_p1,
                            self.demand_p2,
                            self.demand_p3)()
            def lead_times(self):
                    if self.leadtime_dist == "Constant":
                        return self.leadtime_p1
                    elif self.leadtime_dist == "Normal":
                        return make_distribution(
                            np.random.normal,
                            self.leadtime_p1,
                            self.leadtime_p2)()
                    elif self.leadtime_dist == "Triangular":
                        return make_distribution(
                            np.random_triangular,
                            self.leadtime_p1,
                            self.leadtime_p2,
                            self.leadtime_p3)()
            def __repr__(self):
                    return '<Product %r>' % self.name
                                
            def placeorder(product, final_inv_pos, policy, period):                
                #lead_time = int(product.lead_time())
                lead_time = float(datos['Tespera'])
                # Qs = if we hit the reorder point s, order Q units
                if policy['method'] == 'Qs' and \
                        final_inv_pos <= policy['param2']:
                    return policy['param1'], lead_time
                # RS = if we hit the review period R and the reorder point S, order: (S -
                # final inventory pos)
                elif policy['method'] == 'RS' and \
                    period % policy['param1'] == 0 and \
                        final_inv_pos <= policy['param2']:
                    return policy['param2'] - final_inv_pos, lead_time
                else:
                    return 0, 0

            politica = {'method': "Qs",'param1': 50,'param2': 20}
            class Order(object):
                """Object that stores basic data of an order"""
                def __init__(self, quantity, lead_time):
                    self.quantity = quantity
                    self.lead_time = lead_time
            class product(object):
                def __init__ (self,name,price,order_cost,initial_inventory,demand_dist,demand_p1,demand_p2,demand_p3,leadtime_dist,leadtime_p1,leadtime_p2,leadtime_p3):
                    self.name=name
                    self.price=price
                    self.order_cost=order_cost
                    self.initial_inventory=initial_inventory
                    self.demand_dist=demand_dist
                    self.demand_p1=demand_p1
                    self.demand_p2=demand_p2
                    self.demand_p3=demand_p3
                    self.leadtime_dist=leadtime_dist
                    self.leadtime_p1=leadtime_p1
                    self.leadtime_p2=leadtime_p2
                    self.leadtime_p3=leadtime_p3
            producto = product("Mesa", 18.0,20.0,100,"Constant",80.0,0.0,0.0,"Constant",1.0,0.0,0.0)
            df = make_data(producto, politica, period)
                          
            contexto = {'data':dfQ.to_html(classes="table table-striped table-hover text-dark"),
            'datas':df.to_html(classes="table table-striped table-hover text-dark"),  
            'calculos':dfCalculos.to_html(classes="table table-striped table-hover text-dark"),
            'titulo':'Modelo Inventario'}
            return render(request, 'inventario_resultado.html',contexto)
    else:
        return HttpResponseNotFound()

def m_inventario_grafica(request):
    
    df = mi.get_df()
    print(df)
    f = plt.figure()
    df = df.loc[:,'Costo_ordenar':'Costo_total']
    plt.plot(df)
    plt.legend(df.columns, loc="upper left")

    
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(f)
    canvas.print_png(buf)
    
    response = HttpResponse(buf.getvalue(), content_type='image/png')

    f.clear()
    response['Content-Length'] = str(len(response.content))

    return response
    
