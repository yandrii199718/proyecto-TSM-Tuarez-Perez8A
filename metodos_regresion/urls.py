from django.urls import path
from . import views_regresion_lineal
from . import views_regresion_nolineal


urlpatterns = [
    path('regresion_lineal/', views_regresion_lineal.regresion_lineal_cant_muestra),
    path('RL_muestras/',views_regresion_lineal.regresion_lineal_muestras),
    path('RL_resultado/', views_regresion_lineal.regresion_lineal_resultado),
    path('RL_grafico/', views_regresion_lineal.regresion_lineal_grafica),
    #NOLINEAL
    path('regresion_nolineal/', views_regresion_nolineal.regresion_nolineal_cant_muestra),
    path('RNL_muestras/',views_regresion_nolineal.regresion_nolineal_muestras),
    path('RNL_resultado/', views_regresion_nolineal.regresion_nolineal_resultado),
    path('RNL_grafico/', views_regresion_nolineal.regresion_nolineal_grafica)


]