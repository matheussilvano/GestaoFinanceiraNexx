from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Cliente
from django.urls import reverse

class ClienteTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cliente_data = {
            'nome': 'Cliente Teste',
            'cpf': '12345678901',
            'email': 'teste@teste.com'
        }
        self.cliente = Cliente.objects.create(**self.cliente_data)
        self.url = reverse('cliente-list')

    def test_criar_cliente(self):
        """Testa a criação de um cliente"""
        data = {
            'nome': 'Novo Cliente',
            'cpf': '98765432101',
            'email': 'novo@teste.com'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cliente.objects.count(), 2)

    def test_cpf_duplicado(self):
        """Testa que não é possível criar cliente com CPF duplicado"""
        data = self.cliente_data.copy()
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cpf_invalido(self):
        """Testa validação de CPF com formato inválido"""
        data = self.cliente_data.copy()
        data['cpf'] = '123'  # CPF muito curto
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_listar_clientes(self):
        """Testa listagem de clientes"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_atualizar_cliente(self):
        """Testa atualização de cliente"""
        url = reverse('cliente-detail', args=[self.cliente.id])
        data = {'nome': 'Nome Atualizado', 'email': 'atualizado@teste.com'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cliente.refresh_from_db()
        self.assertEqual(self.cliente.nome, 'Nome Atualizado')

    def test_deletar_cliente(self):
        """Testa exclusão de cliente"""
        url = reverse('cliente-detail', args=[self.cliente.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cliente.objects.count(), 0)