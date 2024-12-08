from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .services import RelatorioService
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class RelatorioViewSet(ViewSet):
    @method_decorator(cache_page(60 * 15))  # Cache por 15 minutos
    @action(detail=False, methods=['get'])
    def geral(self, request):
        # Retorna o relatório geral com saldo total, receitas e despesas
        cliente_id = request.query_params.get('cliente_id')
        resultado = RelatorioService.get_relatorio_geral(cliente_id)
        return Response(resultado)

    @method_decorator(cache_page(60 * 15))  # Cache por 15 minutos
    @action(detail=False, methods=['get'])
    def evolucao(self, request):
        # Retorna a evolução de receitas e despesas ao longo do tempo
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        cliente_id = request.query_params.get('cliente_id')
        agrupamento = request.query_params.get('agrupamento', 'dia')
        
        resultado = RelatorioService.get_evolucao_receitas_despesas(
            data_inicio, data_fim, cliente_id, agrupamento
        )
        return Response(resultado)
