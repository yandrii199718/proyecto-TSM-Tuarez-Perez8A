from django.urls import path
from . import views_modelo_real


urlpatterns = [
    path('Rlineas_espera/', views_modelo_real.Rformulario_linea_espera),
    path('Rls_resultado/grafica', views_modelo_real.Rls_grafica),
    path('Rls_resultado/', views_modelo_real.Rlinea_espera_resultado)
    
   
]