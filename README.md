# HelpOP

Sistema para gestão de serviços automotivos, conectando usuários e profissionais.

## Instalação Local

1. Crie e ative um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure o banco de dados PostgreSQL:
   ```bash
   # Copie o arquivo de exemplo
   cp .env.example .env
   
   # Edite o arquivo .env com suas configurações
   # Para desenvolvimento local, use as variáveis DB_*
   # Para produção, use DATABASE_URL
   ```
4. Execute as migrações:
   ```bash
   python manage.py migrate
   ```
5. Crie um superusuário:
   ```bash
   python manage.py createsuperuser
   ```
6. Colete os arquivos estáticos:
   ```bash
   python manage.py collectstatic --noinput
   ```
7. Inicie o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```

## Configuração do Banco de Dados

### Desenvolvimento Local
Para desenvolvimento local, configure as variáveis no arquivo `.env`:

```env
# Para PostgreSQL local
DB_NAME=helpop_db
DB_USER=postgres
DB_PASSWORD=sua_senha_postgres
DB_HOST=localhost
DB_PORT=5432
```

### Produção (Railway)
Para produção, use a `DATABASE_URL` fornecida pelo Railway:

```env
DATABASE_URL=postgres://usuario:senha@host:5432/nome_do_banco
```

### Teste de Conexão
Para testar a conexão com o banco:

```bash
python test_db.py
```

## Deploy no Railway

### 1. Preparação
- Certifique-se de que o código está no GitHub
- O Railway detecta automaticamente o `Procfile` e `requirements.txt`

### 2. Variáveis de Ambiente no Railway
Configure estas variáveis no painel do Railway:

```
DEBUG=False
SECRET_KEY=sua-secret-key-aqui
ALLOWED_HOSTS=railway.app,localhost,127.0.0.1,*.railway.app
DATABASE_URL=postgres://usuario:senha@host:5432/nome_do_banco
```

**Importante:** A `DATABASE_URL` deve ser fornecida pelo Railway automaticamente quando você adiciona um banco PostgreSQL ao projeto.

### 3. Comandos de Deploy
Após o deploy inicial, execute no terminal do Railway:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py compress --force
```

### 4. Estrutura do Projeto
```
helpOP/
├── helpOP/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/
├── templates/
├── static/
├── requirements.txt
├── Procfile
├── runtime.txt
└── test_db.py
```

## Funcionalidades
- Cadastro de usuários (clientes e profissionais)
- Cadastro de veículos
- Histórico de manutenções
- Cadastro de profissionais e serviços
- Avaliação de profissionais
- Dashboard para profissionais
- Sistema de aprovação de profissionais

## Bibliotecas Instaladas

### Principais
- **Django** - Framework web
- **Gunicorn** - Servidor WSGI para produção
- **Whitenoise** - Servir arquivos estáticos
- **Django-environ** - Gerenciar variáveis de ambiente
- **psycopg2-binary** - Conector PostgreSQL

### Otimização
- **Django Compressor** - Comprimir CSS/JS
- **Django Libsass** - Suporte a SASS
- **Pillow** - Processamento de imagens

### Segurança
- **Django CORS Headers** - Configurar CORS

### Cache (Opcional)
- **Redis** - Cache de alta performance
- **Django Redis** - Integração Redis/Django

## Resolução de Problemas

### Erro de Conexão com PostgreSQL
Se aparecer erro `ValueError: Port could not be cast to integer value as 'porta'`:

1. Verifique se a `DATABASE_URL` está correta no Railway
2. Certifique-se de que a porta é um número (normalmente 5432)
3. Execute o teste de conexão: `python test_db.py`

### Erro de Módulo não encontrado
Se aparecer erro de módulo não encontrado, verifique se todas as dependências estão no `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Erro de Configuração
Se houver erro de configuração, verifique se as variáveis de ambiente estão corretas no Railway.

### Arquivos Estáticos
Se houver problemas com arquivos estáticos:

```bash
python manage.py collectstatic --noinput
python manage.py compress --force
``` 