from django.db import models

class Corredor(models.Model):
    nombre = models.CharField(max_length=50) 

    def _str_(self):
        return self.nombre

class Entrada(models.Model):
    TIPO_CHOICES = [
        ('MONTO_BRUTO', 'Monto Bruto'),
        ('FACTOR', 'Factor'),
    ]

    corredor = models.ForeignKey(Corredor, 
                                 on_delete=models.CASCADE, 
                                 related_name='entradas') 
    
    
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    

    monto = models.IntegerField(null=True, blank=True)
    
  
    factor = models.FloatField(null=True, blank=True)
    
   
    tipo_ingreso = models.BooleanField(default=True) 
    
    
    created_at = models.DateTimeField(auto_now_add=True) 

    def _str_(self):
        return f"{self.tipo} - {self.corredor.nombre}"