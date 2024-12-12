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
    def test_cliente_view_filtros_diversos(self):
        """Testa views de clientes com diferentes filtros"""
        url = reverse('cliente-list')
        
        # Testa filtro por nome
        response_nome = self.client.get(f"{url}?search={self.cliente.nome}")
        self.assertEqual(response_nome.status_code, status.HTTP_200_OK)
        
        # Testa filtro por email
        response_email = self.client.get(f"{url}?email={self.cliente.email}")
        self.assertEqual(response_email.status_code, status.HTTP_200_OK)