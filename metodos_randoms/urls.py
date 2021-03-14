from django.urls import path
from . import views_cuadrado_medio
from . import views_aditivo
from . import views_multiplicativo
urlpatterns = [
    path('cuadrado_medio/', views_cuadrado_medio.cuadrado_medio),
    path('CM_resultado/', views_cuadrado_medio.cuadrado_medio_resultado),
    path('CM_resultado/grafica', views_cuadrado_medio.cuadrado_medio_grafica),
    path('metodo_aditivo/', views_aditivo.metodo_aditivo),
    path('aditivo_resultado/', views_aditivo.aditivo_resultado),
    path('aditivo_resultado/grafica', views_aditivo.aditivo_grafica),
    path('metodo_multiplicativo/', views_multiplicativo.metodo_multiplicativo),
    path('multiplicativo_resultado/', views_multiplicativo.multiplicativo_resultado),
    path('multiplicativo_resultado/grafica', views_multiplicativo.multiplicativo_grafica)
]