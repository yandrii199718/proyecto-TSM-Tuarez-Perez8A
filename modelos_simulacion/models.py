from django.db import models
import pandas as pd
# Create your models here.
class LineaDeEspera(models.Model):
    landa = models.FloatField()   
    nu = models.FloatField()
    ri = models.FloatField()
    df = pd.DataFrame()


    def set_df(self, df):
        self.df = df 
           
    def get_df(self):
        return self.df


class ModeloInventario(models.Model):
    demanda = models.FloatField()   
    costoO = models.FloatField()
    costoM = models.FloatField()
    costoP = models.FloatField()
    Tespera = models.FloatField()
    DiasAno = models.FloatField()
    ri = models.FloatField()
    df = pd.DataFrame()


    def set_df(self, df):
        self.df = df
           
    def get_df(self):
        return self.df

class LineaDeEsperaMontecarlo(models.Model):
    cant_tiempo = models.IntegerField()
    tiempo_llegada = models.FloatField()
    cant_servicio = models.IntegerField()
    tiempo_servicio = models.FloatField()
    iteraciones = models.IntegerField()

    cantidad_eventos = models.IntegerField()

    df_tiempo_llegadas = pd.DataFrame()
    df_tiempo_servicio = pd.DataFrame()
    df_resultado =pd.DataFrame()


    def set_df_llegada(self, df):
        self.df_tiempo_llegadas = df
           
    def get_df_llegada(self):
        return self.df_tiempo_llegadas

    def set_df_servicio(self, df):
        self.df_tiempo_servicio = df 
           
    def get_df_servicio(self):
        return self.df_tiempo_servicio

    def set_df_resultado(self, df):
        self.df_resultado = df 
           
    def get_df_resultado(self):
        return self.df_resultado

    def busqueda(self, arrmin, arrmax, valor):
        for i in range(len(arrmin)):
            if valor >= arrmin[i] and valor <= arrmax[i]:
                
                return i
        return -1



    
