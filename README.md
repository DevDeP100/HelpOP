# HelpOP

Sistema para gestão de serviços automotivos, conectando usuários e profissionais.

## Instalação

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

## Estrutura Inicial
- Cadastro de usuários (clientes e profissionais)
- Cadastro de veículos
- Histórico de manutenções
- Cadastro de profissionais e serviços
- Avaliação de profissionais

## Próximos Passos
- Implementar autenticação e permissões
- Criar views e rotas para as funcionalidades principais
- Adicionar testes automatizados 

# Deploy no Railway

1. Faça login no Railway e crie um novo projeto.
2. Adicione as variáveis de ambiente conforme o arquivo `.env.example`.
3. O Railway detecta automaticamente o Procfile e requirements.txt.
4. O comando de start será: `gunicorn helpOP.helpOP.wsgi:application`
5. Certifique-se de rodar as migrações após o deploy:
   ```
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```
6. Pronto! Seu projeto estará disponível no domínio do Railway. 