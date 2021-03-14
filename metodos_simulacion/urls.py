from django.urls import path
from . import views_montecarlo, views_transformada_inversa

urlpatterns = [
    path('montecarlo/', views_montecarlo.formulario_montecarlo),
    path('montecarlo_muestras/', views_montecarlo.formulario_montecarlo_muestras),
    path('montecarlo_eventos/', views_montecarlo.formulario_montecarlo_eventos),
    path('montecarlo_resultado/', views_montecarlo.montecarlo_resultado),
    path('transformada_inversa/', views_transformada_inversa.transformada),
    path('transformada_inversa/grafica/', views_transformada_inversa.transformada_grafico)


]