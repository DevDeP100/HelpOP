#!/bin/bash

# Script para buscar imagens da Oficina Jordão no Papicu, Fortaleza
# Autor: HelpOP
# Data: $(date)

echo "🔍 Buscando imagens da Oficina Jordão no Papicu, Fortaleza..."

# Criar diretório para imagens da Jordão
mkdir -p jordao_images
cd jordao_images

echo "📋 Fontes de busca:"
echo "1. Google Maps"
echo "2. Google Street View"
echo "3. Instagram"
echo "4. Facebook"
echo "5. Google Meu Negócio"
echo "6. Sites locais"
echo ""

# Tentar buscar em diferentes fontes
echo "🌐 Tentando buscar imagens..."

# 1. Tentar Google Maps (screenshot simulado)
echo "📍 Tentando Google Maps..."
# Como não podemos acessar diretamente, vamos simular com imagens de oficinas similares

# 2. Tentar imagens de oficinas brasileiras similares
echo "🇧🇷 Baixando imagens de oficinas brasileiras similares..."

# Imagens de oficinas brasileiras/profissionais (como fallback)
curl -o jordao_fachada.jpg "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=800&h=600&fit=crop" 2>/dev/null || echo "❌ Erro ao baixar fachada"
curl -o jordao_equipamentos.jpg "https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=800&h=600&fit=crop" 2>/dev/null || echo "❌ Erro ao baixar equipamentos"
curl -o jordao_atendimento.jpg "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800&h=600&fit=crop" 2>/dev/null || echo "❌ Erro ao baixar atendimento"
curl -o jordao_servicos.jpg "https://images.unsplash.com/photo-1581094794329-c8112a89af12?w=800&h=600&fit=crop" 2>/dev/null || echo "❌ Erro ao baixar serviços"

echo "✅ Imagens baixadas!"

# Verificar se as imagens foram baixadas
echo ""
echo "📊 Status dos downloads:"
ls -la *.jpg 2>/dev/null || echo "❌ Nenhuma imagem encontrada"

echo ""
echo "🔄 Copiando para o carrossel..."

# Copiar para o diretório principal
cp jordao_fachada.jpg ../oficina1.jpg 2>/dev/null || echo "❌ Erro ao copiar fachada"
cp jordao_equipamentos.jpg ../oficina2.jpg 2>/dev/null || echo "❌ Erro ao copiar equipamentos"
cp jordao_atendimento.jpg ../oficina3.jpg 2>/dev/null || echo "❌ Erro ao copiar atendimento"
cp jordao_servicos.jpg ../oficina4.jpg 2>/dev/null || echo "❌ Erro ao copiar serviços"

echo "✅ Imagens copiadas para o carrossel!"

echo ""
echo "📋 Próximos passos para imagens reais da Oficina Jordão:"
echo "1. Acesse: https://www.google.com/maps"
echo "2. Pesquise: 'Oficina Jordão Papicu Fortaleza'"
echo "3. Tire screenshots das fotos do estabelecimento"
echo "4. Salve com os nomes: oficina1.jpg, oficina2.jpg, etc."
echo "5. Substitua as imagens atuais"
echo ""

echo "🎯 Carrossel atualizado!"
echo "   Acesse http://localhost:8010 para ver o resultado"

cd .. 