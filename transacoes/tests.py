from django.test import TestCase
from django.utils import timezone
from transacoes.models import Transacao
from clientes.models import Cliente

class TransacaoModelTests(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nome='Cliente Teste',
            cpf='12345678901',
            email='teste@teste.com'
        )

    def test_transacao_criar_receita(self):
        """Teste de criação de transação de receita"""
        transacao = Transacao.objects.create(
            cliente=self.cliente,
            data_hora=timezone.now(),
            valor=100.00,
            tipo='receita',
            descricao='Receita Teste',
            categoria='salario'
        )
        
        self.assertEqual(transacao.valor, 100.00)
        self.assertEqual(transacao.tipo, 'receita')

    def test_transacao_criar_despesa(self):
        """Teste de criação de transação de despesa"""
        transacao = Transacao.objects.create(
            cliente=self.cliente,
            data_hora=timezone.now(),
            valor=50.00,
            tipo='despesa',
            descricao='Despesa Teste',
            categoria='alimentacao'
        )
        
        self.assertEqual(transacao.valor, -50.00)
        self.assertEqual(transacao.tipo, 'despesa')

    def test_transacao_str_representation(self):
        """Teste da representação em string da transação"""
        transacao = Transacao.objects.create(
            cliente=self.cliente,
            data_hora=timezone.now(),
            valor=75.50,
            tipo='receita',
            descricao='Representação Teste',
            categoria='outros'
        )
        
        # Verifica se a representação em string contém informações importantes
        str_repr = str(transacao)
        self.assertIn(transacao.descricao, str_repr)
        self.assertIn(str(transacao.valor), str_repr)

    def test_transacao_campos_obrigatorios(self):
        """Teste de campos obrigatórios"""
        with self.assertRaises(Exception):
            Transacao.objects.create(
                cliente=self.cliente,
                # Deixando campos obrigatórios em branco
                tipo='receita'
            )

    def test_transacao_tipos_validos(self):
        """Teste de validação de tipos de transação"""
        with self.assertRaises(Exception):
            Transacao.objects.create(
                cliente=self.cliente,
                data_hora=timezone.now(),
                valor=100.00,
                tipo='investimento',  # Tipo inválido
                descricao='Teste Tipo Inválido',
                categoria='outros'
            )