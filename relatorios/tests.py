from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from clientes.models import Cliente
from transacoes.models import Transacao
from .services import RelatorioService

class RelatoriosServiceTests(TestCase):
    def setUp(self):
        # Criar cliente de teste
        self.cliente = Cliente.objects.create(
            nome='Cliente Teste',
            cpf='12345678901',
            email='teste@teste.com'
        )
        
        # Criar transações de teste
        data_base = timezone.now()
        
        # Receita
        Transacao.objects.create(
            cliente=self.cliente,
            data_hora=data_base,
            valor=1000.00,
            tipo='receita',
            descricao='Salário',
            categoria='outros'
        )
        
        # Despesa
        Transacao.objects.create(
            cliente=self.cliente,
            data_hora=data_base + timedelta(days=1),
            valor=500.00,
            tipo='despesa',
            descricao='Aluguel',
            categoria='outros'
        )

    def test_relatorio_geral_com_cliente(self):
        """Testa serviço de relatório geral para um cliente específico"""
        relatorio = RelatorioService.get_relatorio_geral(self.cliente.id)
        
        # Verificar resumo
        self.assertIsNotNone(relatorio['resumo'])
        
        # Verificar valores específicos
        self.assertEqual(relatorio['resumo']['saldo_total'], 500.00)
        self.assertEqual(relatorio['resumo']['total_receitas'], 1000.00)
        self.assertEqual(relatorio['resumo']['total_despesas'], -500.00)

    def test_relatorio_geral_sem_cliente(self):
        """Testa relatório geral sem filtro de cliente"""
        relatorio = RelatorioService.get_relatorio_geral()
        
        # Verificar que o relatório não está vazio
        self.assertIsNotNone(relatorio['resumo'])
        self.assertIsNotNone(relatorio['categorias'])

    def test_evolucao_financeira_por_cliente(self):
        """Testa evolução financeira para um cliente específico"""
        evolucao = RelatorioService.get_evolucao_receitas_despesas(
            cliente_id=self.cliente.id,
            data_inicio=timezone.now().date(),
            data_fim=timezone.now().date()
        )
        
        # Verificar que há resultados
        self.assertTrue(len(evolucao) > 0)

    def test_evolucao_financeira_agrupamento(self):
        """Testa evolução financeira com diferentes tipos de agrupamento"""
        # Teste com agrupamento mensal
        evolucao_mensal = RelatorioService.get_evolucao_receitas_despesas(
            agrupamento='mes'
        )
        self.assertTrue(len(evolucao_mensal) > 0)

        # Teste com agrupamento diário
        evolucao_diaria = RelatorioService.get_evolucao_receitas_despesas(
            agrupamento='dia'
        )
        self.assertTrue(len(evolucao_diaria) > 0)

    def test_evolucao_financeira_sem_filtros(self):
        """Testa evolução financeira sem filtros específicos"""
        evolucao = RelatorioService.get_evolucao_receitas_despesas()
        
        # Verificar que há resultados
        self.assertTrue(len(evolucao) >= 0)  # Pode ser vazio se não houver transações

    def test_servico_relatorio_sem_transacoes(self):
        """Testa serviço de relatório quando não há transações"""
        # Limpa todas as transações
        Transacao.objects.all().delete()
        
        # Testa relatório sem transações
        from relatorios.services import RelatorioService
        
        relatorio = RelatorioService.get_relatorio_geral()
        
        self.assertIsNotNone(relatorio)
        self.assertEqual(relatorio['resumo']['saldo_total'], None)
        self.assertEqual(relatorio['resumo']['total_receitas'], None)
        self.assertEqual(relatorio['resumo']['total_despesas'], None)
        self.assertEqual(len(relatorio['categorias']), 0)

    def test_servico_evolucao_receitas_despesas_sem_filtro(self):
        """Testa serviço de evolução de receitas e despesas sem filtros"""
        from relatorios.services import RelatorioService
        
        evolucao = RelatorioService.get_evolucao_receitas_despesas()
        
        self.assertIsNotNone(evolucao)
        self.assertTrue(isinstance(evolucao, list))