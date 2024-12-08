from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone
from django.db.models import F, Q
from datetime import datetime
from .models import Transacao
from .serializers import TransacaoSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page 

class TransacaoViewSet(viewsets.ModelViewSet):
    queryset = Transacao.objects.all()
    serializer_class = TransacaoSerializer

    @method_decorator(cache_page(60 * 15))
    @action(detail=False, methods=['get'])
    def evolucao_financeira(self, request):
        # Pega parâmetros da query
        cpf = request.query_params.get('cliente_cpf')
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        agrupamento = request.query_params.get('agrupamento', 'mes')

        # Base query
        queryset = self.get_queryset()

        # Aplica filtros
        if cpf:
            queryset = queryset.filter(cliente__cpf=cpf)
        if data_inicio:
            queryset = queryset.filter(data_hora__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_hora__lte=data_fim)

        # Define função de truncamento baseado no agrupamento
        trunc_func = TruncMonth if agrupamento == 'mes' else TruncDate

        # Agrupa e calcula valores
        evolucao = queryset.annotate(
            periodo=trunc_func('data_hora')
        ).values('periodo').annotate(
            receitas=Sum('valor', filter=Q(tipo='receita')),
            despesas=Sum('valor', filter=Q(tipo='despesa')),
        ).order_by('periodo')

        # Formata resposta
        dados = []
        for entry in evolucao:
            dados.append({
                'periodo': entry['periodo'].strftime('%Y-%m-%d'),
                'receitas': float(entry['receitas'] or 0),
                'despesas': abs(float(entry['despesas'] or 0)),  # Converte para positivo para visualização
                'saldo': float((entry['receitas'] or 0) + (entry['despesas'] or 0))
            })

        return Response({
            'dados': dados,
            'filtros_aplicados': {
                'cliente_cpf': cpf,
                'data_inicio': data_inicio,
                'data_fim': data_fim,
                'agrupamento': agrupamento
            }
        })
    
    @method_decorator(cache_page(60 * 15))
    @action(detail=False, methods=['get'])
    def relatorio_geral(self, request):
        """
        Retorna o relatório geral com saldo total, receitas e despesas agregados por cliente.
        """
        cliente_id = request.query_params.get('cliente_id')
        queryset = self.get_queryset()
        
        if cliente_id:
            queryset = queryset.filter(cliente_id=cliente_id)
            
        # Calcula resumo geral
        resumo = queryset.aggregate(
            saldo_total=Sum('valor'),
            total_receitas=Sum('valor', filter=Q(tipo='receita')),
            total_despesas=Sum('valor', filter=Q(tipo='despesa'))
        )
        
        # Agrupa por categoria
        categorias = queryset.values('categoria').annotate(
            total=Sum('valor')
        ).order_by('categoria')
        
        return Response({
            'resumo': {
                'saldo_total': float(resumo['saldo_total'] or 0),
                'total_receitas': float(resumo['total_receitas'] or 0),
                'total_despesas': float(resumo['total_despesas'] or 0)
            },
            'categorias': list(categorias)
        })
