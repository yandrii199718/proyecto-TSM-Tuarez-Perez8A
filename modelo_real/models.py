from django.db import models
import pandas as pd
# Create your models here.
class RLineaDeEspera(models.Model):
    landa = models.FloatField()   
    nu = models.FloatField()
    ri = models.FloatField()
    df = pd.DataFrame()


    def set_df(self, df):
        self.df = df 
           
    def get_df(self):
        return self.df
