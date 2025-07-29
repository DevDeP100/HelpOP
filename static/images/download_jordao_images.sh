#!/bin/bash

# Script para baixar imagens da Oficina Jordão
# Autor: HelpOP
# Data: $(date)

echo "🚗 Baixando imagens da Oficina Jordão para o carrossel..."

# Criar backup das imagens atuais
echo "📦 Fazendo backup das imagens atuais..."
cp oficina1.jpg oficina1_backup.jpg
cp oficina2.jpg oficina2_backup.jpg
cp oficina3.jpg oficina3_backup.jpg
cp oficina4.jpg oficina4_backup.jpg

echo "✅ Backup criado com sucesso!"

# Opção 1: Baixar imagens da Oficina Jordão (se você tiver as URLs)
echo ""
echo "🔍 Para usar imagens da Oficina Jordão:"
echo "1. Obtenha as URLs das imagens da oficina"
echo "2. Execute os comandos abaixo:"
echo ""

echo "# Exemplo de comandos para baixar imagens da Oficina Jordão:"
echo "# Substitua as URLs pelas reais da Oficina Jordão"
echo ""
echo "curl -o oficina1.jpg 'URL_DA_FACHADA_DA_OFICINA_JORDAO'"
echo "curl -o oficina2.jpg 'URL_DOS_EQUIPAMENTOS_DA_OFICINA_JORDAO'"
echo "curl -o oficina3.jpg 'URL_DO_ATENDIMENTO_DA_OFICINA_JORDAO'"
echo "curl -o oficina4.jpg 'URL_DOS_SERVICOS_DA_OFICINA_JORDAO'"
echo ""

# Opção 2: Usar imagens temporárias de oficinas brasileiras
echo "🔄 Baixando imagens temporárias de oficinas brasileiras..."
echo "   (Estas são imagens profissionais enquanto você busca as da Oficina Jordão)"

# Imagens de oficinas brasileiras/profissionais
curl -o oficina1.jpg "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=800&h=600&fit=crop"
curl -o oficina2.jpg "https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=800&h=600&fit=crop"
curl -o oficina3.jpg "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800&h=600&fit=crop"
curl -o oficina4.jpg "https://images.unsplash.com/photo-1581094794329-c8112a89af12?w=800&h=600&fit=crop"

echo "✅ Imagens temporárias baixadas!"
echo ""

echo "📋 Próximos passos:"
echo "1. Entre em contato com a Oficina Jordão"
echo "2. Peça autorização para usar as imagens"
echo "3. Substitua as imagens temporárias pelas da Oficina Jordão"
echo "4. Execute: python manage.py collectstatic"
echo ""

echo "🔄 Para restaurar as imagens originais:"
echo "cp oficina1_backup.jpg oficina1.jpg"
echo "cp oficina2_backup.jpg oficina2.jpg"
echo "cp oficina3_backup.jpg oficina3.jpg"
echo "cp oficina4_backup.jpg oficina4.jpg"
echo ""

echo "🎯 Carrossel atualizado com imagens profissionais!"
echo "   Acesse http://localhost:8010 para ver o resultado" 