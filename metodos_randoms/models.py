from django.db import models

class CuadradoMedio(models.Model):
    semilla = models.FloatField()
    iteraciones = models.IntegerField()
    ri = models.FloatField()

    def set_ri(self, ri):
        self.ri = ri
    
    def get_ri(self):
        return self.ri

        
    

class Aditivo(models.Model):
    semilla = models.FloatField()
    multiplicador = models.FloatField()
    incremento = models.FloatField()
    modulo = models.FloatField()
    ri = models.FloatField()

    def set_ri(self, ri):
        self.ri = ri
    
    def get_ri(self):
        return self.ri
    

class Multiplicativo(models.Model):
    moderna = models.FloatField()   
    semilla = models.FloatField()
    incremento = models.FloatField()
    
    def set_ri(self, ri):
        self.ri = ri
    
    def get_ri(self):
        return self.ri