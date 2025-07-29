# Dependências do Projeto HelpOP

## **📦 Visão Geral**

Este documento lista todas as dependências do projeto HelpOP, organizadas por categoria e funcionalidade.

## **🔧 Dependências Principais**

### **Django e Core**
- **Django==5.2.4** - Framework web principal
- **asgiref==3.9.1** - Interface ASGI para Django
- **sqlparse==0.5.3** - Parser SQL para Django

### **API e REST**
- **djangorestframework==3.16.0** - Framework REST API
- **drf-yasg==1.21.10** - Geração automática de documentação Swagger
- **PyYAML==6.0.2** - Parser YAML para Swagger
- **uritemplate==4.2.0** - Templates de URI para OpenAPI
- **inflection==0.5.1** - Inflexão de strings para APIs

### **Banco de Dados**
- **psycopg2==2.9.10** - Driver PostgreSQL
- **psycopg2-binary==2.9.10** - Driver PostgreSQL (binário)

### **Email e Comunicação**
- **django-anymail==13.0.1** - Backend de email unificado
- **secure-smtplib==0.1.1** - SMTP seguro
- **certifi==2025.7.14** - Certificados SSL/TLS

### **Arquivos Estáticos e Frontend**
- **django-compressor==4.5.1** - Compressão de arquivos estáticos
- **django-libsass==0.9** - Compilação SASS/SCSS
- **libsass==0.23.0** - Compilador SASS
- **whitenoise==6.9.0** - Servir arquivos estáticos
- **CairoSVG==2.8.2** - Conversão SVG
- **cairocffi==1.7.1** - Bindings Cairo
- **cssselect2==0.8.0** - Seletores CSS
- **tinycss2==1.4.0** - Parser CSS
- **webencodings==0.5.1** - Codificações web
- **defusedxml==0.7.1** - XML seguro
- **rcssmin==1.1.2** - Minificação CSS
- **rjsmin==1.2.2** - Minificação JavaScript

### **Configuração e Ambiente**
- **django-environ==0.12.0** - Gerenciamento de variáveis de ambiente
- **django-dotenv==1.4.2** - Carregamento de .env
- **python-dotenv==1.1.1** - Carregamento de .env (Python)
- **django-appconf==1.1.0** - Configuração de apps Django

### **CORS e Segurança**
- **django-cors-headers==4.7.0** - Headers CORS
- **charset-normalizer==3.4.2** - Normalização de charset
- **idna==3.10** - Internacionalização de nomes de domínio

### **Cache e Performance**
- **django-redis==6.0.0** - Cache Redis para Django
- **redis==6.2.0** - Cliente Redis

### **HTTP e Requisições**
- **requests==2.32.4** - Biblioteca HTTP
- **urllib3==2.5.0** - Cliente HTTP

### **Utilitários**
- **packaging==25.0** - Utilitários de empacotamento
- **pytz==2025.2** - Fuso horário
- **setuptools==80.9.0** - Ferramentas de configuração
- **wheel==0.45.1** - Formato de distribuição Python

### **Desenvolvimento e Debug**
- **django-debug-toolbar==6.0.0** - Toolbar de debug
- **pillow==11.3.0** - Processamento de imagens

### **Deploy e Produção**
- **gunicorn==23.0.0** - Servidor WSGI para produção

## **🚀 Instalação**

### **Instalar todas as dependências:**
```bash
pip install -r requirements.txt
```

### **Instalar apenas dependências de desenvolvimento:**
```bash
pip install django-debug-toolbar pillow
```

### **Instalar apenas dependências de produção:**
```bash
pip install django djangorestframework drf-yasg psycopg2-binary gunicorn whitenoise
```

## **📋 Categorias de Dependências**

### **🟢 Essenciais (Produção)**
- Django
- Django REST Framework
- drf-yasg
- psycopg2-binary
- gunicorn
- whitenoise
- django-environ

### **🟡 Importantes (Funcionalidades)**
- django-compressor
- django-cors-headers
- django-anymail
- redis
- requests

### **🟠 Opcionais (Desenvolvimento)**
- django-debug-toolbar
- pillow
- django-libsass

### **🔴 Utilitárias (Suporte)**
- PyYAML
- uritemplate
- inflection
- packaging
- pytz

## **🔧 Configuração por Ambiente**

### **Desenvolvimento:**
```bash
pip install -r requirements.txt
```

### **Produção:**
```bash
pip install django djangorestframework drf-yasg psycopg2-binary gunicorn whitenoise django-environ django-compressor django-cors-headers
```

### **Testes:**
```bash
pip install django-debug-toolbar pillow
```

## **📊 Versões e Compatibilidade**

### **Django 5.2.4:**
- ✅ Compatível com Python 3.8+
- ✅ Suporte LTS até abril de 2026
- ✅ Todas as dependências testadas

### **Django REST Framework 3.16.0:**
- ✅ Compatível com Django 5.2
- ✅ Suporte completo a OpenAPI 3.0
- ✅ Integração com drf-yasg

### **drf-yasg 1.21.10:**
- ✅ Geração automática de Swagger
- ✅ Suporte a Django 5.2
- ✅ Documentação interativa

## **🔍 Verificação de Dependências**

### **Verificar dependências instaladas:**
```bash
pip list
```

### **Verificar dependências desatualizadas:**
```bash
pip list --outdated
```

### **Atualizar requirements.txt:**
```bash
pip freeze > requirements.txt
```

## **🚨 Dependências Críticas**

### **Para API REST:**
- `djangorestframework` - Framework REST
- `drf-yasg` - Documentação Swagger
- `PyYAML` - Parser YAML

### **Para Banco de Dados:**
- `psycopg2-binary` - Driver PostgreSQL

### **Para Deploy:**
- `gunicorn` - Servidor WSGI
- `whitenoise` - Arquivos estáticos

### **Para Email:**
- `django-anymail` - Backend de email
- `secure-smtplib` - SMTP seguro

## **🎉 Dependências Atualizadas!**

O arquivo `requirements.txt` está **100% atualizado** com todas as dependências necessárias! ✨📦 