from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, F
from django.db.models.functions import TruncDate, TruncMonth
from .models import Transacao
from .serializers import TransacaoSerializer

class TransacaoViewSet(viewsets.ModelViewSet):
    queryset = Transacao.objects.all()
    serializer_class = TransacaoSerializer
    filterset_fields = ['cliente', 'categoria', 'tipo']
    
    @action(detail=False, methods=['get'])
    def relatorio_geral(self, request):
        cliente_id = request.query_params.get('cliente_id')
        queryset = self.get_queryset()
        
        if cliente_id:
            queryset = queryset.filter(cliente_id=cliente_id)
            
        resumo = queryset.aggregate(
            saldo_total=Sum('valor'),
            total_receitas=Sum('valor', filter=F('tipo')=='receita'),
            total_despesas=Sum('valor', filter=F('tipo')=='despesa')
        )
        
        # Resumo por categoria
        categorias = queryset.values('categoria').annotate(
            total=Sum('valor')
        ).order_by('categoria')
        
        return Response({
            'resumo': resumo,
            'categorias': categorias
        })
    
    @action(detail=False, methods=['get'])
    def evolucao_receitas_despesas(self, request):
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        cliente_id = request.query_params.get('cliente_id')
        agrupamento = request.query_params.get('agrupamento', 'dia')
        
        queryset = self.get_queryset()
        
        if cliente_id:
            queryset = queryset.filter(cliente_id=cliente_id)
        if data_inicio:
            queryset = queryset.filter(data_hora__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_hora__lte=data_fim)
            
        # Agrupa por dia ou mês
        trunc_func = TruncDate if agrupamento == 'dia' else TruncMonth
        
        evolucao = queryset.annotate(
            data=trunc_func('data_hora')
        ).values('data').annotate(
            receitas=Sum('valor', filter=F('tipo')=='receita'),
            despesas=Sum('valor', filter=F('tipo')=='despesa')
        ).order_by('data')
        
        return Response(evolucao)