from django.db import models
from django.core.validators import RegexValidator

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(
        max_length=11, 
        unique=True,
        validators=[RegexValidator(
            regex=r'^\d{11}$',
            message='CPF deve conter exatamente 11 dígitos numéricos'
        )]
    )
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.cpf}"