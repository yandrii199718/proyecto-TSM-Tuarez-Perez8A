from django.urls import path
from . import views_lineas_espera
from . import views_inventario
from . import views_lineas_espera_montecarlo

urlpatterns = [
    path('lineas_espera/', views_lineas_espera.formulario_linea_espera),
    path('ls_resultado/grafica', views_lineas_espera.ls_grafica),
    path('ls_resultado/', views_lineas_espera.linea_espera_resultado),
    path('m_inventario/', views_inventario.formulario_inventario),
    path('m_inventario/grafica', views_inventario.m_inventario_grafica),
    path('m_inventario_resultado/', views_inventario.m_inventario_resultado),

    path('lineas_espera_montecarlo/',views_lineas_espera_montecarlo.cantidad_tiempo),
    path('lineas_espera_montecarlo_servicio/',views_lineas_espera_montecarlo.cantidad_servicio),
    path('LE_montecarlo/',views_lineas_espera_montecarlo.lineas_montecarlo_resultado),
    



]