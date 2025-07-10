from django.db import models

class Edificio(models.Model):
    RESIDENCIAL = 'residencial'
    COMERCIAL = 'comercial'
    TIPOS = [
        (RESIDENCIAL, 'Residencial'),
        (COMERCIAL, 'Comercial')
    ]

    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS)

    def __str__(self):
        return f"{self.nombre} - {self.direccion} - {self.ciudad} - {self.tipo}"

class Departamento(models.Model):
    propietario = models.CharField(max_length=100)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    cuartos = models.IntegerField()
    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE, related_name='departamentos')

    def __str__(self):
        return f"{self.propietario} - {self.costo} -{self.cuartos} - {self.edificio.nombre}"

