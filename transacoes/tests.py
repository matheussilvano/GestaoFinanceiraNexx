from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Transacao
from clientes.models import Cliente
from django.utils import timezone
from decimal import Decimal

class TransacaoTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cliente = Cliente.objects.create(
            nome='Cliente Teste',
            cpf='12345678901',
            email='teste@teste.com'
        )
        self.transacao_data = {
            'cliente': self.cliente.id,
            'data_hora': timezone.now().isoformat(),
            'valor': '100.00',
            'tipo': 'receita',
            'descricao': 'Teste',
            'categoria': 'outros'
        }
        self.transacao = Transacao.objects.create(
            cliente=self.cliente,
            data_hora=timezone.now(),
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