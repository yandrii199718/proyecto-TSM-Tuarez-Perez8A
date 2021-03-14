from django.db import models
import pandas as pd


class Montercarlo(models.Model):
    cantidad = models.IntegerField()
    muestra = models.FloatField()
    cantidad_eventos = models.IntegerField()

    def set_muestras(self, muestra):
        self.muestra = muestra

    def get_muestras(self):
        return self.muestra
    
    def busqueda(self, arrmin, arrmax, valor):
        for i in range (len(arrmin)):
            if valor >= arrmin[i] and valor <= arrmax[i]:
                
                return i
        return -1

class Transformada(models.Model):
    lambd = models.FloatField()
    df = pd.DataFrame()

    def set_df(self, df):
        self.df = df 
           
    def get_df(self):
        return self.df


