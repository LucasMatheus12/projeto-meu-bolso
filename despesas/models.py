from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
class Categoria(models.Model):
    nome = models.CharField(max_length=120)
    descricao = models.TextField(blank = True,null= True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Despesa(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    def clean(self):
        if self.valor < 0:
            raise ValidationError('O valor da despesa não pode ser negativo.')

class Deposito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    descricao = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.descricao} - {self.valor:.2f}'

    def clean(self):
        if self.valor < 0:
            raise ValidationError('O valor do depósito não pode ser negativo.')