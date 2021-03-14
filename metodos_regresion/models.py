from django.db import models

class RegresionLineal(models.Model):
    cantidad = models.IntegerField()
    valor = models.FloatField()
    x = models.FloatField()
    p = models.FloatField()


    def set_valor(self, valor):
        self.valor = valor
    
    def get_valor(self):
        return self.valor

    def set_p(self, p):
        self.p = p
    
    def get_p(self):
        return self.p

    def set_x(self, x):
        self.x = x
    
    def get_x(self):
        return self.x

class RegresionNoLineal(models.Model):
    cantidad = models.IntegerField()
    valor = models.FloatField()
    x = models.FloatField()
    p = models.FloatField()


    def set_valor(self, valor):
        self.valor = valor
    
    def get_valor(self):
        return self.valor

    def set_p(self, p):
        self.p = p
    
    def get_p(self):
        return self.p

    def set_x(self, x):
        self.x = x
    
    def get_x(self):
        return self.x
