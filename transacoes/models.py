from django.db import models
from django.core.validators import MinValueValidator
from clientes.models import Cliente

class Transacao(models.Model):
    CATEGORIA_CHOICES = [
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
        validators=[MinValueValidator(0.01)]
    )
    descricao = models.CharField(max_length=200)
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIA_CHOICES
    )
    tipo = models.CharField(
        max_length=8,
        choices=[('receita', 'Receita'), ('despesa', 'Despesa')]
    )

    def save(self, *args, **kwargs):
        if self.tipo == 'despesa':
            self.valor = -abs(self.valor)
        else:
            self.valor = abs(self.valor)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-data_hora']