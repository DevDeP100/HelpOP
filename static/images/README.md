# Imagens de Oficinas

## Arquivos Necessários

Para que o carrossel funcione corretamente, você precisa adicionar as seguintes imagens:

1. `oficina1.jpg` - Imagem de oficina automotiva
2. `oficina2.jpg` - Imagem de oficina automotiva
3. `oficina3.jpg` - Imagem de oficina automotiva
4. `oficina4.jpg` - Imagem de oficina automotiva

## URLs de Exemplo (Imagens Gratuitas)

### Oficina 1 - Oficina Moderna
- **URL**: https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=800&h=600&fit=crop
- **Descrição**: Oficina automotiva moderna com equipamentos profissionais
- **Download**: `wget https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=800&h=600&fit=crop -O oficina1.jpg`

### Oficina 2 - Área de Serviço
- **URL**: https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=800&h=600&fit=crop
- **Descrição**: Área de serviço com ferramentas e equipamentos
- **Download**: `wget https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=800&h=600&fit=crop -O oficina2.jpg`

### Oficina 3 - Elevador Automotivo
- **URL**: https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800&h=600&fit=crop
- **Descrição**: Elevador automotivo com veículo em manutenção
- **Download**: `wget https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800&h=600&fit=crop -O oficina3.jpg`

### Oficina 4 - Ferramentas Profissionais
- **URL**: https://images.unsplash.com/photo-1581094794329-c8112a89af12?w=800&h=600&fit=crop
- **Descrição**: Ferramentas profissionais de oficina automotiva
- **Download**: `wget https://images.unsplash.com/photo-1581094794329-c8112a89af12?w=800&h=600&fit=crop -O oficina4.jpg`

## Como Baixar as Imagens

### Opção 1: Usando wget (Linux/Mac)
```bash
cd static/images/
wget "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=800&h=600&fit=crop" -O oficina1.jpg
wget "https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=800&h=600&fit=crop" -O oficina2.jpg
wget "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800&h=600&fit=crop" -O oficina3.jpg
wget "https://images.unsplash.com/photo-1581094794329-c8112a89af12?w=800&h=600&fit=crop" -O oficina4.jpg
```

### Opção 2: Usando curl (Linux/Mac)
```bash
cd static/images/
curl -o oficina1.jpg "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=800&h=600&fit=crop"
curl -o oficina2.jpg "https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=800&h=600&fit=crop"
curl -o oficina3.jpg "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800&h=600&fit=crop"
curl -o oficina4.jpg "https://images.unsplash.com/photo-1581094794329-c8112a89af12?w=800&h=600&fit=crop"
```

### Opção 3: Download Manual
1. Acesse cada URL no navegador
2. Clique com botão direito na imagem
3. Selecione "Salvar imagem como..."
4. Salve com o nome correto (oficina1.jpg, oficina2.jpg, etc.)

## Especificações Recomendadas

- **Formato**: JPG
- **Dimensões**: 800x600px (proporção 4:3)
- **Tamanho**: Máximo 500KB por imagem
- **Conteúdo**: Imagens de oficinas automotivas profissionais

## Carrossel

O carrossel alterna automaticamente a cada 3 segundos e inclui:
- Navegação com setas
- Indicadores de pontos
- Efeitos de hover
- Design responsivo
- Altura: 400px
- Largura: 120% do container

## Fonte das Imagens

Todas as imagens são do **Unsplash**, que oferece fotos gratuitas de alta qualidade para uso comercial e não comercial. 