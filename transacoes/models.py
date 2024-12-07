from django.db import models
from django.core.validators import MinValueValidator
from clientes.models import Cliente
from decimal import Decimal

class Transacao(models.Model):
    CATEGORIAS = [
        ('alimentacao', 'Alimentação'),
        ('transporte', 'Transporte'),
        ('lazer', 'Lazer'),
        ('outros', 'Outros'),
    ]

    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.PROTECT,
        related_name='transacoes'
    )
    data_hora = models.DateTimeField()
    valor = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    tipo = models.CharField(
        max_length=10,
        choices=[('receita', 'Receita'), ('despesa', 'Despesa')]
    )
    descricao = models.CharField(max_length=200)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)

    def save(self, *args, **kwargs):
        if self.tipo == 'despesa':
            self.valor = -abs(self.valor)
        else:
            self.valor = abs(self.valor)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-data_hora']