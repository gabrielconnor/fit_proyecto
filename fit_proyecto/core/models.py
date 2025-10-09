from django.db import models

class Corredor(models.Model):
    nombre = models.CharField(max_length=50) 

    def _str_(self):
        return self.nombre

# ----------------------------------------------------

class Entrada(models.Model):
    TIPO_CHOICES = [
        ('MONTO_BRUTO', 'Monto Bruto'),
        ('FACTOR', 'Factor'),
    ]

    # OPCIONES DE DIVISA RESTRINGIDAS (NUEVAS)
    DIVISA_CHOICES = [
        ('CLP', 'Peso Chileno ($)'),
        ('PEN', 'Sol Peruano (S/)'),
        ('COP', 'Peso Colombiano ($)'),
    ]

    corredor = models.ForeignKey(Corredor, 
                                 on_delete=models.CASCADE, 
                                 related_name='entradas') 
    
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    
    # CAMPO DE DIVISA
    divisa = models.CharField(
        max_length=3,           # Máximo 3 caracteres para el código ISO
        choices=DIVISA_CHOICES,
        default='CLP',          # Puedes establecer un valor predeterminado diferente si es necesario
        help_text="Tipo de divisa: CLP, PEN o COP."
    )
    
    monto = models.IntegerField(null=True, blank=True)
    factor = models.FloatField(null=True, blank=True)
    tipo_ingreso = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True) 

    def _str_(self):
        return f"{self.tipo} - {self.corredor.nombre} ({self.divisa})"