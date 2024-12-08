from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Transacao
from clientes.models import Cliente
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

def create_aware_datetime(year, month, day, hour=0, minute=0, second=0):
    """Helper para criar datetime com timezone"""
    return timezone.make_aware(
        datetime(year, month, day, hour, minute, second),
        timezone=timezone.get_current_timezone()
    )

class TransacaoTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cliente = Cliente.objects.create(
            nome='Cliente Teste',
            cpf='12345678901',
            email='teste@teste.com'
        )
        
        # Usando datas fixas para teste
        self.data_atual = create_aware_datetime(2024, 12, 7)
        
        self.transacao_data = {
            'cliente': self.cliente.id,
            'data_hora': self.data_atual.isoformat(),
            'valor': '100.00',
            'tipo': 'receita',
            'descricao': 'Teste',
            'categoria': 'outros'
        }
        
        self.transacao = Transacao.objects.create(
            cliente=self.cliente,
            data_hora=self.data_atual,
            valor=100.00,
            tipo='receita',
            descricao='Teste',
            categoria='outros'
        )
        self.url = reverse('transacao-list')

    def test_criar_transacao(self):
        """Testa criação de transação"""
        data = self.transacao_data.copy()
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transacao.objects.count(), 2)

    def test_criar_transacao_valor_negativo(self):
        """Testa que não permite valor negativo direto"""
        data = self.transacao_data.copy()
        data['valor'] = '-100.00'
        data['tipo'] = 'receita'
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_criar_despesa(self):
        """Testa criação de despesa"""
        data = self.transacao_data.copy()
        data['tipo'] = 'despesa'
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        transacao = Transacao.objects.get(id=response.data['id'])
        self.assertTrue(transacao.valor < 0)  # Valor deve ser negativo para despesas

    def test_listar_transacoes(self):
        """Testa listagem de transações"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filtrar_por_cliente(self):
        """Testa filtro de transações por cliente"""
        url = f"{self.url}?cliente={self.cliente.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_atualizar_transacao(self):
        """Testa atualização de transação"""
        url = reverse('transacao-detail', args=[self.transacao.id])
        data = {'descricao': 'Descrição atualizada'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.transacao.refresh_from_db()
        self.assertEqual(self.transacao.descricao, 'Descrição atualizada')

    def test_deletar_transacao(self):
        """Testa exclusão de transação"""
        url = reverse('transacao-detail', args=[self.transacao.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Transacao.objects.count(), 0)

    def test_relatorio_geral(self):
        """Testa relatório geral de transações"""
        # Cria uma segunda transação para ter dados mais significativos
        data_segunda_transacao = create_aware_datetime(2024, 12, 7, 12, 0, 0)
        Transacao.objects.create(
            cliente=self.cliente,
            data_hora=data_segunda_transacao,
            valor=200.00,
            tipo='receita',
            descricao='Outro teste',
            categoria='alimentacao'
        )

        url = reverse('transacao-relatorio-geral')
        
        # Testa sem filtros
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('resumo', response.data)
        self.assertIn('categorias', response.data)
        
        # Testa com filtro de cliente
        response = self.client.get(f"{url}?cliente_id={self.cliente.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('resumo', response.data)

    def test_evolucao_receitas_despesas(self):
        """Testa evolução de receitas e despesas"""
        # Usando datas fixas para teste
        data_antiga = create_aware_datetime(2024, 11, 7)
        data_inicio = create_aware_datetime(2024, 10, 7)
        data_fim = create_aware_datetime(2024, 12, 7, 23, 59, 59)

    def test_evolucao_financeira(self):
        """Testa endpoint de evolução financeira"""
        # Cria algumas transações de teste
        Transacao.objects.create(
            cliente=self.cliente,
            data_hora=timezone.now(),
            valor=1000.00,
            tipo='receita',
            descricao='Salário',
            categoria='outros'
        )
        Transacao.objects.create(
            cliente=self.cliente,
            data_hora=timezone.now(),
            valor=-500.00,
            tipo='despesa',
            descricao='Aluguel',
            categoria='outros'
        )

        # Testa endpoint
        url = reverse('transacao-evolucao-financeira')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica estrutura da resposta
        self.assertIn('dados', response.data)
        self.assertIn('filtros_aplicados', response.data)
        
        # Verifica se os dados estão corretos
        dados = response.data['dados']
        self.assertTrue(len(dados) > 0)
        self.assertIn('periodo', dados[0])
        self.assertIn('receitas', dados[0])
        self.assertIn('despesas', dados[0])
        self.assertIn('saldo', dados[0])

        # Testa filtros
        params = {
            'cliente_cpf': self.cliente.cpf,
            'agrupamento': 'dia'
        }
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Cria transação antiga
        Transacao.objects.create(
            cliente=self.cliente,
            data_hora=data_antiga,
            valor=300.00,
            tipo='receita',
            descricao='Receita antiga',
            categoria='outros'
        )
        
        # Cria transação recente
        Transacao.objects.create(
            cliente=self.cliente,
            data_hora=data_fim,
            valor=150.00,
            tipo='despesa',
            descricao='Despesa recente',
            categoria='alimentacao'
        )

        url = reverse('transacao-evolucao-receitas-despesas')
        
        # Testa sem filtros
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Testa com todos os filtros
        params = {
            'cliente_id': self.cliente.id,
            'data_inicio': data_inicio.date().isoformat(),
            'data_fim': data_fim.date().isoformat(),
            'agrupamento': 'mes'
        }
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

