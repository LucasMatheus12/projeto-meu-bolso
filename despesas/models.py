from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nome = models.CharField(max_length=120)
    descricao = models.TextField(blank = True,null= True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Despesa(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True,null=True)
    data = models.DateField()
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10,decimal_places=2)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome