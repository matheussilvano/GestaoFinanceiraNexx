# Sistema de Gestão de Transações Financeiras
![Linguagem](https://img.shields.io/badge/Linguagem-Python-blue?style=flat-square&logo=python)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow?style=flat-square)
![Banco de Dados](https://img.shields.io/badge/Banco%20de%20Dados-PostgreSQL-blue?style=flat-square&logo=postgresql)
![Framework](https://img.shields.io/badge/Framework-Django-green?style=flat-square&logo=django)

## Descrição do Projeto
Sistema backend robusto para gerenciamento de dados financeiros de clientes, com funcionalidades completas de CRUD, geração de relatórios e análises gráficas.

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

## Configuração do Ambiente

### Clonar o Repositório
```bash
git clone https://github.seu-usuario/financas-backend.git
cd financas-backend
```

### Configurar Ambiente de Desenvolvimento
```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### Iniciar Ambiente com Docker
```bash
docker-compose up --build
```

### Executar Migrações
```bash
docker-compose exec web python manage.py migrate
```

### Executar Testes
```bash
docker-compose exec web pytest
```

## Documentação da API
Acesse a documentação Swagger em: `http://localhost:8000/swagger/`

## Estrutura do Projeto
```
financas-backend/
│
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
