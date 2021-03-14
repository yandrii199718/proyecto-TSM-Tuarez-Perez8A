"""tecnicas_simulacion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

from tecnicas_simulacion import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('metodos_probabilisticos/', include('metodos_probabilisticos.urls')),
    path('metodos_randoms/', include('metodos_randoms.urls')),
    path('metodos_regresion/', include('metodos_regresion.urls')),
    path('metodos_simulacion/', include('metodos_simulacion.urls')),
    path('modelos_simulacion/', include('modelos_simulacion.urls')),
    path('modelo_real/', include('modelo_real.urls')),
    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
