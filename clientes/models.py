from django.db import models
from django.core.validators import RegexValidator

class Cliente(models.Model):
    cpf = models.CharField(
        max_length=14, 
        unique=True, 
        validators=[RegexValidator(
            regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', 
            message='CPF deve estar no formato 000.000.000-00'
        )]
    )
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.cpf}"
