from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from clientes.models import Cliente
from transacoes.models import Transacao

class RelatoriosTests(TestCase):
    def setUp(self):
        self.client = APIClient()
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

    def test_relatorio_geral(self):
        url = reverse('relatorio-geral')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertIn('resumo', data)
        self.assertIn('categorias', data)
        
        resumo = data['resumo']
        self.assertEqual(resumo['saldo_total'], 500.00)  # 1000 - 500
        self.assertEqual(resumo['total_receitas'], 1000.00)
        self.assertEqual(resumo['total_despesas'], -500.00)

    def test_evolucao_receitas_despesas(self):
        url = reverse('relatorio-evolucao')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertTrue(len(data) >= 2)  # Deve ter pelo menos 2 dias