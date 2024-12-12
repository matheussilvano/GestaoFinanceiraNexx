#!/bin/bash

echo -e "\033[1;34m=== CRIAÇÃO DO SUPER-USUÁRIO ===\033[0m"
read -p "Informe o nome de usuário: " USERNAME
read -p "Informe o e-mail: " EMAIL
read -sp "Informe a senha: " PASSWORD
echo

echo -e "\033[1;33m[STATUS]\033[0m Criando superusuário no container Docker..."

docker-compose exec web python manage.py createsuperuser \
    --username "$USERNAME" \
    --email "$EMAIL"

if [ $? -eq 0 ]; then
    echo -e "\033[1;32m[SUCESSO]\033[0m Super-usuário criado com sucesso!"
else
    echo -e "\033[1;31m[ERRO]\033[0m Falha ao criar o super-usuário."
    exit 1
fi

echo -e "\033[1;33m[STATUS]\033[0m Realizando autenticação via API..."

# URL da API
URL="http://localhost:8000/api/token/"

RESPONSE=$(curl -s -X POST "$URL" \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}")

if echo "$RESPONSE" | grep -q "refresh"; then
    TOKEN_REFRESH=$(echo "$RESPONSE" | jq -r '.refresh')
    TOKEN_ACCESS=$(echo "$RESPONSE" | jq -r '.access')
    
    echo -e "\033[1;32m[SUCESSO]\033[0m Autenticação bem-sucedida!"
    echo -e "\033[1;36mToken Refresh:\033[0m $TOKEN_REFRESH"
    echo -e "\033[1;36mToken Access:\033[0m $TOKEN_ACCESS"
    
else
    echo -e "\033[1;31m[ERRO]\033[0m Falha na autenticação via API."
    echo "Resposta da API: $RESPONSE"
fi
