#!/bin/bash

# Script de inicialização para Railway
echo "🚀 Iniciando HelpOP..."

# Coletar arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Executar migrações
echo "🗄️ Executando migrações..."
python manage.py migrate

# Iniciar servidor
echo "🌐 Iniciando servidor..."
gunicorn wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120 