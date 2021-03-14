from django.urls import path
from . import views,  views_metodo_promedio_movil, views_alisamiento

urlpatterns = [
    path('promedio_movil/', views_metodo_promedio_movil.promedio_movil),
    path('PM_valor_muestras/', views_metodo_promedio_movil.form_valor_muestra),
    path('PM_dominio/', views_metodo_promedio_movil.form_dominio),
    path('PM_resultado/', views_metodo_promedio_movil.promedio_movil2),
    path('PM_resultado/grafico/', views_metodo_promedio_movil.mostrar_grafico),

    
    #Alisamiento   
    path('alisamiento_exp/', views_alisamiento.alisamiento_exponencial),
    path('AEX_valor_muestras/', views_alisamiento.form_alisamiento_muestra),
    path('AEX_alfa/', views_alisamiento.form_alisamiento_dominio),
    path('AEX_resultado/', views_alisamiento.alisamiento_resultado),
    path('AEX_grafico/',views_alisamiento.alisamiento_grafica)

]