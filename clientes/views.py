from rest_framework import viewsets
from .models import Cliente
from .serializers import ClienteSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filterset_fields = ['nome', 'cpf']
    search_fields = ['nome', 'cpf', 'email']
    ordering_fields = ['nome', 'created_at']
    
    def destroy(self, request, *args, **kwargs):
        cliente = self.get_object()
        if Transacao.objects.filter(cliente=cliente).exists():
            return Response(
                {'error': 'Não é possível excluir cliente com transações associadas'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)