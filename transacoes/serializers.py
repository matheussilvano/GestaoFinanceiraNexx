from rest_framework import serializers
from .models import Transacao
from clientes.models import Cliente

class TransacaoSerializer(serializers.ModelSerializer):
    cliente_cpf = serializers.CharField(write_only=True)
    cliente_nome = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Transacao
        fields = [
            'id', 'cliente_cpf', 'cliente_nome', 
            'valor', 'tipo', 'descricao', 
            'categoria', 'data_hora'
        ]
        read_only_fields = ['id', 'data_hora', 'cliente_nome']

    def validate_cliente_cpf(self, value):
        try:
            return Cliente.objects.get(cpf=value)
        except Cliente.DoesNotExist:
            raise serializers.ValidationError("Cliente não encontrado")

    def create(self, validated_data):
        cliente_cpf = validated_data.pop('cliente_cpf')
        cliente = Cliente.objects.get(cpf=cliente_cpf)
        transacao = Transacao.objects.create(cliente=cliente, **validated_data)
        return transacao

    def get_cliente_nome(self, obj):
        return obj.cliente.nome
