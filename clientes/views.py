from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Cliente
from .serializers import ClienteSerializer
from transacoes.models import Transacao 

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filterset_fields = ['nome', 'cpf']
    
    def destroy(self, request, *args, **kwargs):
        cliente = self.get_object()
        if Transacao.objects.filter(cliente=cliente).exists():
            return Response(
                {'error': 'Não é possível excluir cliente com transações associadas'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)