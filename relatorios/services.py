from django.db.models import Sum, F, Case, When, Value, DecimalField
from django.db.models.functions import TruncDate, TruncMonth
from transacoes.models import Transacao

class RelatorioService:
    @staticmethod
    def get_relatorio_geral(cliente_id=None):
        queryset = Transacao.objects.all()
        
        if cliente_id:
            queryset = queryset.filter(cliente_id=cliente_id)
            
        resumo = queryset.aggregate(
            saldo_total=Sum('valor'),
            total_receitas=Sum(Case(
                When(tipo='receita', then='valor'),
                default=Value(0),
                output_field=DecimalField(),
            )),
            total_despesas=Sum(Case(
                When(tipo='despesa', then='valor'),
                default=Value(0),
                output_field=DecimalField(),
            ))
        )
        
        # Resumo por categoria
        categorias = queryset.values('categoria').annotate(
            total=Sum('valor')
        ).order_by('categoria')
        
        return {
            'resumo': resumo,
            'categorias': list(categorias)
        }

    @staticmethod
    def get_evolucao_receitas_despesas(data_inicio=None, data_fim=None, cliente_id=None, agrupamento='dia'):
        queryset = Transacao.objects.all()
        
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
            receitas=Sum(Case(
                When(tipo='receita', then='valor'),
                default=Value(0),
                output_field=DecimalField(),
            )),
            despesas=Sum(Case(
                When(tipo='despesa', then='valor'),
                default=Value(0),
                output_field=DecimalField(),
            ))
        ).order_by('data')
        
        return list(evolucao)
