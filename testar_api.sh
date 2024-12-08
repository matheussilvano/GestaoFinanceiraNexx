#!/bin/bash

# Cores para o output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "=== Iniciando teste da API ==="

# 1. Obtém o token JWT
echo -e "\n${GREEN}1. Obtendo token JWT${NC}"
TOKEN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "silvano", "password": "12345"}')

ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | grep -o '"access":"[^"]*' | grep -o '[^"]*$')

if [ -z "$ACCESS_TOKEN" ]; then
    echo -e "${RED}Erro ao obter token${NC}"
    exit 1
fi

echo "Token obtido com sucesso"

# 2. Cria cliente
echo -e "\n${GREEN}2. Criando cliente${NC}"
curl -X POST http://localhost:8000/api/clientes/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Cliente Teste",
    "cpf": "12345678901",
    "email": "teste@teste.com"
  }'

# 3. Cria transação (receita)
echo -e "\n${GREEN}3. Criando transação (receita)${NC}"
curl -X POST http://localhost:8000/api/transacoes/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "cliente": 1,
    "data_hora": "2024-01-01T10:00:00Z",
    "valor": 1000.00,
    "tipo": "receita",
    "descricao": "Salário",
    "categoria": "outros"
  }'

# 4. Cria transação (despesa)
echo -e "\n${GREEN}4. Criando transação (despesa)${NC}"
curl -X POST http://localhost:8000/api/transacoes/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "cliente": 1,
    "data_hora": "2024-01-05T15:00:00Z",
    "valor": 500.00,
    "tipo": "despesa",
    "descricao": "Aluguel",
    "categoria": "outros"
  }'

# 5. Gera relatório geral
echo -e "\n${GREEN}5. Buscando relatório geral${NC}"
curl -X GET http://localhost:8000/api/transacoes/relatorio_geral/?cliente_id=1 \
  -H "Authorization: Bearer $ACCESS_TOKEN" | json_pp

# 6. Gera relatório de evolução financeira
echo -e "\n${GREEN}6. Buscando evolução financeira${NC}"
curl -X GET "http://localhost:8000/api/transacoes/evolucao_financeira/?cliente_cpf=12345678901&data_inicio=2024-01-01&data_fim=2024-12-31&agrupamento=mes" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | json_pp
