# Configuração de Email - HelpOP

## 📧 Sistema de Verificação de Email

O HelpOP agora inclui um sistema completo de verificação de email para novos usuários. Quando um usuário se cadastra, ele recebe um código de verificação por email que deve ser inserido para ativar a conta.

## 🔧 Configuração para Desenvolvimento

Atualmente, o sistema está configurado para **desenvolvimento** usando o backend de console do Django. Isso significa que os emails aparecem no terminal onde o servidor está rodando.

### Configuração Atual (Desenvolvimento):
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## 🚀 Configuração para Produção

Para usar em produção, você precisa configurar um servidor SMTP real. Aqui estão as opções:

### 1. Gmail (Recomendado para testes)

1. Ative a verificação em duas etapas na sua conta Google
2. Gere uma "Senha de App" específica para o Django
3. Configure no `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'seu-email@gmail.com'
EMAIL_HOST_PASSWORD = 'sua-senha-de-app'
DEFAULT_FROM_EMAIL = 'HelpOP <noreply@helpop.com.br>'
```

### 2. SendGrid (Recomendado para produção)

1. Crie uma conta no SendGrid
2. Configure o domínio de envio
3. Use as configurações:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'sua-api-key-do-sendgrid'
DEFAULT_FROM_EMAIL = 'HelpOP <noreply@helpop.com.br>'
```

### 3. Amazon SES

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'sua-access-key'
EMAIL_HOST_PASSWORD = 'sua-secret-key'
DEFAULT_FROM_EMAIL = 'HelpOP <noreply@helpop.com.br>'
```

## 🔒 Variáveis de Ambiente (Recomendado)

Para maior segurança, use variáveis de ambiente:

```python
import os

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'HelpOP <noreply@helpop.com.br>')
```

## 📋 Como Funciona o Sistema

### 1. Cadastro do Usuário
- Usuário preenche o formulário de cadastro
- Sistema cria a conta (inicialmente não verificada)
- Sistema gera um código de 6 dígitos
- Email é enviado com o código

### 2. Verificação de Email
- Usuário acessa a página de verificação
- Insere o código recebido
- Sistema valida o código
- Conta é marcada como verificada

### 3. Login
- Sistema verifica se o email foi confirmado
- Se não confirmado, redireciona para verificação
- Se confirmado, permite o login

## 🧪 Testando o Sistema

1. Acesse: http://localhost:8000/cadastro/
2. Preencha o formulário com um email válido
3. Verifique o terminal do servidor para ver o email
4. Copie o código e acesse a página de verificação
5. Insira o código para confirmar a conta

## 🔧 Personalização

### Modificar o Template de Email
Edite o arquivo `core/email_utils.py` para personalizar o email.

### Alterar Tempo de Expiração
No modelo `CodigoVerificacao`, modifique o método `expirado()`:

```python
def expirado(self):
    # Alterar de 24 horas para outro valor
    return timezone.now() > self.data_criacao + timedelta(hours=1)  # 1 hora
```

### Modificar o Tamanho do Código
No modelo `CodigoVerificacao`, altere o método `gerar_codigo()`:

```python
def gerar_codigo(self):
    # Alterar de 6 para 8 dígitos, por exemplo
    return ''.join(random.choices(string.digits, k=8))
```

## 🚨 Troubleshooting

### Email não está sendo enviado
1. Verifique as configurações SMTP
2. Confirme se as credenciais estão corretas
3. Teste com o backend de console primeiro

### Código não está sendo validado
1. Verifique se o código não expirou (24 horas)
2. Confirme se o código não foi usado anteriormente
3. Verifique se o usuário está correto

### Usuário não consegue fazer login
1. Verifique se o email foi confirmado (`email_verificado = True`)
2. Confirme se o usuário existe no banco de dados
3. Verifique se a senha está correta

## 📞 Suporte

Para dúvidas sobre a configuração de email, consulte:
- [Documentação do Django - Email](https://docs.djangoproject.com/en/stable/topics/email/)
- [SendGrid Documentation](https://sendgrid.com/docs/)
- [Gmail SMTP Settings](https://support.google.com/mail/answer/7126229) 