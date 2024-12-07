# Sistema de Gestão de Transações Financeiras
![Linguagem](https://img.shields.io/badge/Linguagem-Python-blue?style=flat-square&logo=python)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow?style=flat-square)
![Banco de Dados](https://img.shields.io/badge/Banco%20de%20Dados-PostgreSQL-blue?style=flat-square&logo=postgresql)
![Framework](https://img.shields.io/badge/Framework-Django-green?style=flat-square&logo=django)

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
git clone [URL_DO_SEU_REPOSITORIO]
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
docker-compose exec web python manage.py migrate
```

4. Crie um superusuário:
```bash
docker-compose exec web python manage.py createsuperuser
```

## Uso

Após a instalação, você pode acessar:

- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/
- Documentação da API: http://localhost:8000/swagger/

### Endpoints Principais

- `/api/clientes/`: CRUD de clientes
- `/api/transacoes/`: CRUD de transações
- `/api/transacoes/relatorio_geral/`: Relatório geral de transações
- `/api/transacoes/evolucao_receitas_despesas/`: Evolução de receitas e despesas

## Testes

Para executar os testes:

```bash
# Todos os testes
docker-compose exec web python manage.py test

# Testes específicos
docker-compose exec web python manage.py test clientes.tests
docker-compose exec web python manage.py test transacoes.tests
docker-compose exec web python manage.py test relatorios.tests

# Cobertura de testes
docker-compose exec web coverage run --source='.' manage.py test
docker-compose exec web coverage report
```

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

## Andamento do projeto
# Sistema de Gestão de Transações Financeiras

## Implementação das Funcionalidades

### CRUD de Clientes
- [x] Implementado
  - Arquivos:
    - `clientes/models.py`
    - `clientes/views.py`
    - `app/urls.py`

### Cadastro de Transações
- [x] Implementado
  - Arquivos:
    - `transacoes/models.py`
    - `transacoes/views.py`
    - `app/urls.py`

### Relatórios
- [x] Relatório Geral Implementado
  - Arquivos:
    - `reports/views.py`
- [ ] Gráficos Pendente

### Validações e Regras
- [x] Implementado
  - Arquivos:
    - `clientes/models.py`
    - `transacoes/models.py`

### Testes Automatizados
- [ ] Não Implementado

### Documentação
- [x] Presente
  - Arquivos:
    - `README.md`

## Próximos Passos
- [ ] Adicionar autenticação
- [ ] Criar mais testes para ampliar cobertura e complexidade
- [ ] Implementar relatórios pendentes
- [ ] Adicionar validações mais complexas

