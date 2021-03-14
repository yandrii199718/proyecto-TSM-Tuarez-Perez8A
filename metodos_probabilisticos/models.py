from django.db import models


class PromedioMovil(models.Model):
    muestra = models.IntegerField()
    valor = models.FloatField()
    dominio = models.IntegerField()
    MM_3 = models.FloatField()
    MM_4 = models.FloatField()
    
    def set_values(self, valor):
        self.valor = valor

    def get_values(self):
        return self.valor
    
    def set_mm3(self, mm_3):
        self.MM_3 = mm_3
    
    def get_mm3(self):
        return self.MM_3

    def set_mm4(self, mm_4):
        self.MM_4 = mm_4

    def get_mm4(self):
        return self.MM_4


class  MuestraAlisamiento(models.Model):
    muestra = models.IntegerField()
    valor = models.FloatField()
    dominio = models.FloatField()
    suavizacion = models.FloatField()

    def set_values(self, valor):
        self.valor = valor

    def get_values(self):
        return self.valor

    def set_suavizacion(self, suavizacion):
        self.suavizacion = suavizacion
    
    def get_suavizacion(self):
        return self.suavizacion

