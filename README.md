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
3. Execute as migrações:
   ```bash
   python manage.py migrate
   ```
4. Crie um superusuário:
   ```bash
   python manage.py createsuperuser
   ```
5. Inicie o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
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
DATABASE_URL=postgres://usuario:senha@host:porta/nome_do_banco
```

### 3. Comandos de Deploy
Após o deploy inicial, execute no terminal do Railway:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
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
├── requirements.txt
├── Procfile
└── runtime.txt
```

## Funcionalidades
- Cadastro de usuários (clientes e profissionais)
- Cadastro de veículos
- Histórico de manutenções
- Cadastro de profissionais e serviços
- Avaliação de profissionais
- Dashboard para profissionais
- Sistema de aprovação de profissionais 