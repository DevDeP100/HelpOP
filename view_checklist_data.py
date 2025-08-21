#!/usr/bin/env python
"""
Script para criar uma view simples para visualizar os dados de checklist
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpOP.settings')
django.setup()

from core.models import CategoriaChecklist, ItemChecklist
from django.http import HttpResponse
from django.template import Template, Context

def generate_checklist_html():
    """Gerar HTML com os dados de checklist"""
    
    html_template = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dados de Checklist Automotivo - HelpOP</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .category-card { 
            border-left: 4px solid #ffc107; 
            margin-bottom: 2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .category-header {
            background: linear-gradient(135deg, #ffc107 0%, #ffb300 100%);
            color: #000;
            font-weight: bold;
        }
        .item-list {
            max-height: 400px;
            overflow-y: auto;
        }
        .item-badge {
            background-color: #e9ecef;
            color: #495057;
            font-size: 0.85rem;
        }
        .stats-card {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
        }
    </style>
</head>
<body>
    <div class="container py-5">
        <div class="row mb-4">
            <div class="col-12">
                <div class="text-center">
                    <h1 class="display-4 text-warning mb-3">
                        <i class="fas fa-clipboard-list me-3"></i>
                        Dados de Checklist Automotivo
                    </h1>
                    <p class="lead text-muted">Sistema HelpOP - Base de dados populada com sucesso</p>
                </div>
            </div>
        </div>
        
        <!-- Estatísticas -->
        <div class="row mb-5">
            <div class="col-md-6">
                <div class="card stats-card">
                    <div class="card-body text-center">
                        <i class="fas fa-folder-open fa-3x mb-3"></i>
                        <h3 class="card-title">{{ total_categorias }}</h3>
                        <p class="card-text">Categorias de Checklist</p>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card stats-card">
                    <div class="card-body text-center">
                        <i class="fas fa-tasks fa-3x mb-3"></i>
                        <h3 class="card-title">{{ total_itens }}</h3>
                        <p class="card-text">Itens de Verificação</p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Categorias e Itens -->
        {% for categoria in categorias %}
        <div class="card category-card">
            <div class="card-header category-header">
                <div class="row align-items-center">
                    <div class="col">
                        <h4 class="mb-0">
                            <i class="fas fa-cog me-2"></i>
                            {{ categoria.ordem }}. {{ categoria.nome }}
                        </h4>
                        <small class="text-dark">{{ categoria.descricao }}</small>
                    </div>
                    <div class="col-auto">
                        <span class="badge bg-dark">{{ categoria.total_itens }} itens</span>
                    </div>
                </div>
            </div>
            <div class="card-body">
                <div class="item-list">
                    <div class="row">
                        {% for item in categoria.itens %}
                        <div class="col-md-6 mb-2">
                            <div class="d-flex align-items-center">
                                <span class="badge item-badge me-2">{{ item.ordem }}</span>
                                <span class="flex-grow-1">{{ item.nome }}</span>
                                {% if item.critico %}
                                <i class="fas fa-exclamation-triangle text-danger ms-2" title="Item Crítico"></i>
                                {% endif %}
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
        {% endfor %}
        
        <div class="text-center mt-5">
            <p class="text-muted">
                <i class="fas fa-check-circle text-success me-2"></i>
                Base de dados populada com sucesso! Acesse o painel administrativo para gerenciar os dados.
            </p>
            <a href="/admin/" class="btn btn-warning me-2">
                <i class="fas fa-cog me-2"></i>Painel Admin
            </a>
            <a href="/checklist/" class="btn btn-primary">
                <i class="fas fa-clipboard-check me-2"></i>Ver Checklists
            </a>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
    """
    
    # Buscar dados
    categorias = CategoriaChecklist.objects.filter(ativo=True).order_by('ordem')
    total_categorias = categorias.count()
    total_itens = ItemChecklist.objects.filter(ativo=True).count()
    
    # Preparar dados para o template
    categorias_data = []
    for categoria in categorias:
        itens = categoria.itens.filter(ativo=True).order_by('ordem')
        categorias_data.append({
            'ordem': categoria.ordem,
            'nome': categoria.nome,
            'descricao': categoria.descricao,
            'total_itens': itens.count(),
            'itens': [{
                'ordem': item.ordem,
                'nome': item.nome,
                'critico': item.critico
            } for item in itens]
        })
    
    # Renderizar template
    template = Template(html_template)
    context = Context({
        'total_categorias': total_categorias,
        'total_itens': total_itens,
        'categorias': categorias_data
    })
    
    return template.render(context)

if __name__ == '__main__':
    print("🚗 Gerando visualização dos dados de checklist...")
    
    html_content = generate_checklist_html()
    
    # Salvar arquivo HTML
    output_file = '/Users/danielnogueira/Documents/Desenvolvimento/HelpOP/checklist_data_view.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Arquivo HTML gerado: {output_file}")
    print("📱 Abra o arquivo no navegador para visualizar os dados")