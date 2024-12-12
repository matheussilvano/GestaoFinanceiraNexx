# Sistema de Gestão de Transações Financeiras
![Linguagem](https://img.shields.io/badge/Linguagem-Python-blue?style=flat-square&logo=python)
![Status](https://img.shields.io/badge/Status-Concluido-green?style=flat-square)
![Banco de Dados](https://img.shields.io/badge/Banco%20de%20Dados-PostgreSQL-blue?style=flat-square&logo=postgresql)
![Framework](https://img.shields.io/badge/Framework-Django-green?style=flat-square&logo=django)
![Cobertura de Testes](https://img.shields.io/badge/coverage-88%25-brightgreen?style=flat-square&logo=pytest)
![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=flat-square&logo=docker)

## Descrição do Projeto
Sistema backend para gerenciamento de dados financeiros de clientes, com funcionalidades completas de CRUD, geração de relatórios e análises gráficas.

## Funcionalidades
- CRUD completo de Clientes
- Registro e gerenciamento de Transações Financeiras
- Geração de relatórios financeiros
- Gráficos de evolução de receitas e despesas
- Validações de negócio robustas

## Tecnologias Utilizadas
- **Linguagem**: Python
- **Framework**: Django
- **Banco de Dados**: PostgreSQL
- **Containerização**: Docker
- **Testes**: Pytest
- **Documentação da API**: Swagger
- **Autenticação**: JWT (JSON Web Token)

## Requisitos
- Python
- Docker
- Docker Compose

# Sistema de Gestão de Transações Financeiras

Sistema backend desenvolvido em Django para gerenciar e consultar dados financeiros de clientes, incluindo transações, relatórios e análises gráficas.

## Pré-requisitos

- Docker
- Docker Compose
- Git

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/matheussilvano/GestaoFinanceiraNexx.git
cd GestaoFinanceiraNexx
```

2. Execute o projeto:
```bash
# Construir e iniciar os containers
docker-compose up --build

# Ou para rodar em segundo plano
docker-compose up -d
```

3. Execute as migrações do banco de dados:
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

4. Crie um superusuário:
```bash
docker-compose exec web python manage.py createsuperuser
```

## Testes
```bash
# Todos os testes
docker-compose exec web python -m pytest

# Cobertura de testes
docker-compose exec web coverage run -m pytest
docker-compose exec web coverage report
```

### Caso queira realizar um teste prático:
Esse script Shell automatiza o teste da API, realizando etapas como autenticação, criação de clientes e transações, e geração de relatórios. Ele utiliza a ferramenta curl para fazer requisições HTTP.
1. Dê permissão de execução do script de testes:
```bash
chmod +x testar_api.sh
```
2. Execute o script:
```bash
./testar_api.sh
```

## Uso

### Autenticação JWT
Antes de usar a API, você precisa obter um token de acesso:
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "seu_usuario", "password": "sua_senha"}' # Dados utilizados na criação do superusuário
```

Após a criação do Token, use-o nas requisições:
```bash
curl http://localhost:8000/api/clientes/ \
  -H "Authorization: Bearer seu_token_aqui"
```

### Acesso às interfaces

- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/
- Documentação da API: http://localhost:8000/swagger/

### Endpoints Principais

- `/api/token/`: Obter tokens JWT
- `/api/token/refresh/`: Renovar token JWT
- `/api/clientes/`: CRUD de clientes
- `/api/transacoes/`: CRUD de transações
- `/api/transacoes/relatorio_geral/`: Relatório geral de transações
- `/api/transacoes/evolucao_receitas_despesas/`: Evolução de receitas e despesas


## Comandos Úteis

```bash
# Parar os containers
docker-compose down

# Ver logs
docker-compose logs -f

# Acessar o shell do Django
docker-compose exec web python manage.py shell

# Criar novas migrações
docker-compose exec web python manage.py makemigrations
```


## Estrutura do Projeto
```bash
GestaoFinanceiraNexx/
├── app/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── clientes/
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── tests.py
│
├── transacoes/
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── tests.py
│
├── relatorios/
│   ├── __init__.py
│   ├── services.py
│   ├── views.py
│   └── tests.py
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

# Andamento do projeto
## Implementação das Funcionalidades
### CRUD de Clientes
- [x] Implementado
  - Arquivos:
    - `clientes/models.py`: Modelo com validações de CPF e campos obrigatórios
    - `clientes/views.py`: ViewSet com operações CRUD e validações de negócio
    - `clientes/serializers.py`: Serialização e validação de dados
    - `app/urls.py`: Configuração de rotas
### Cadastro de Transações
- [x] Implementado
  - Arquivos:
    - `transacoes/models.py`: Modelo com validações de valor e categorias
    - `transacoes/views.py`: ViewSet com operações CRUD e relatórios
    - `transacoes/serializers.py`: Serialização e validação de transações
    - `app/urls.py`: Configuração de rotas
### Relatórios
- [x] Relatório Geral Implementado
  - `transacoes/views.py`: Endpoints para relatórios
    - Saldo total por cliente
    - Resumo por categoria
    - Evolução temporal de receitas/despesas
- [x] Gráficos Implementados
  - Endpoint para evolução de receitas vs. despesas
  - Suporte a agrupamento por dia/mês
  - Filtros por período e cliente
### Validações e Regras
- [x] Implementado
  - CPF único e formato válido
  - Validação de valores de transação
  - Proteção contra exclusão de clientes com transações
  - Categorização de transações
### Testes Automatizados
- [x] Implementado
  - Arquivos:
    - `clientes/tests.py`: Testes de CRUD e validações
    - `transacoes/tests.py`: Testes de transações e relatórios
    - `relatorios/tests.py`: Testes específicos de relatórios
  - Cobertura atual: 88%
  - 
### Documentação
- [x] Presente
  - `README.md`: Instruções de instalação e uso
  - Swagger: Documentação da API
## Próximos Passos
- [x] Implementar autenticação JWT
- [x] Adicionar cache para otimizar relatórios

## Testes realizados via terminal para validação do funcionamento da API
1. Cadastro de cliente:
```bash
curl -X POST http://localhost:8000/api/clientes/ \
  -H "Content-Type: application/json" \
  -d '{"nome": "João da Silva", "cpf": "12345678901", "email": "joao@exemplo.com"}'
```
2. Listagem de clientes:
```bash
# Lista básica
curl http://localhost:8000/api/clientes/

# Com paginação
curl http://localhost:8000/api/clientes/?page=1

# Filtrar por CPF
curl http://localhost:8000/api/clientes/?cpf=12345678901
```

3. Criar transações:
```bash
# Criar Receita (Positivo)
curl -X POST http://localhost:8000/api/transacoes/ \
  -H "Content-Type: application/json" \
  -d '{
    "cliente": 1,
    "data_hora": "2024-01-01T10:00:00Z",
    "valor": 1000.00,
    "tipo": "receita",
    "descricao": "Salário",
    "categoria": "outros"
  }'

# Criar Despesa (Negativo)
curl -X POST http://localhost:8000/api/transacoes/ \
  -H "Content-Type: application/json" \
  -d '{
    "cliente": 1,
    "data_hora": "2024-01-05T15:00:00Z",
    "valor": 500.00,
    "tipo": "despesa",
    "descricao": "Aluguel",
    "categoria": "outros"
  }'
```

4. Relatórios:
```bash
# Relatório Geral
curl http://localhost:8000/api/transacoes/relatorio_geral/?cliente_id=1

# Evolução Financeira
curl "http://localhost:8000/api/transacoes/evolucao_financeira/?cliente_cpf=12345678901&data_inicio=2024-01-01&data_fim=2024-12-31&agrupamento=mes"
```

5. Testes de validação:
```
# Tentar criar cliente com CPF duplicado
curl -X POST http://localhost:8000/api/clientes/ \
  -H "Content-Type: application/json" \
  -d '{"nome": "Maria Silva", "cpf": "12345678901", "email": "maria@exemplo.com"}'

# Tentar excluir cliente com transações
curl -X DELETE http://localhost:8000/api/clientes/1/
```

