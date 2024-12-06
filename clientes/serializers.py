from rest_framework import serializers
from .models import Cliente

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'cpf', 'nome', 'email', 'data_criacao']
        read_only_fields = ['id', 'data_criacao']
