from django.db import models
from django.core.validators import MinValueValidator
from clientes.models import Cliente

class Categoria(models.TextChoices):
    ALIMENTACAO = 'ALM', 'Alimentação'
    TRANSPORTE = 'TRP', 'Transporte'
    LAZER = 'LZR', 'Lazer'
    OUTROS = 'OTR', 'Outros'

class Transacao(models.Model):
    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.PROTECT, 
        related_name='transacoes'
    )
    valor = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    tipo = models.CharField(
        max_length=1, 
        choices=[('R', 'Receita'), ('D', 'Despesa')]
    )
    descricao = models.TextField()
    categoria = models.CharField(
        max_length=3, 
        choices=Categoria.choices,
        default=Categoria.OUTROS
    )
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente.nome} - {self.valor} - {self.get_tipo_display()}"
