from django.db import models
from django.utils.timezone import now

class Usuario(models.Model):
    nome = models.CharField(max_length = 255)
    email = models.EmailField(unique = True)
    senha = models.CharField(max_length = 100)
    foto = models.ImageField(upload_to='usuarios/')

    def __str__(self):
        return self.nome
    
class Curso(models.Model):
    nome = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    duracao = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    foto = models.ImageField(upload_to='curso/')
    quantidade_estoque = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nome

class Login(models.Model):
    usuario = models.CharField(max_length=255)
    email = models.EmailField()
    senha = models.CharField(max_length=16)

class Foto(models.Model):
    nome = models.CharField(max_length=255)
    foto = models.ImageField(upload_to='imagens/')

class Vendas(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='vendas')
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE, related_name='vendas')
    quantidade = models.PositiveIntegerField()
    data_compra = models.DateTimeField(default=now)

def __str__(self):
    return self.usuario