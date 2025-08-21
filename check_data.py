#!/usr/bin/env python
"""
Script para verificar os dados de checklist na base de dados
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpOP.settings')
django.setup()

from core.models import CategoriaChecklist, ItemChecklist

def check_data():
    print("🔍 Verificando dados na base de dados...")
    print("=" * 50)
    
    # Contar registros
    categorias_count = CategoriaChecklist.objects.count()
    itens_count = ItemChecklist.objects.count()
    
    print(f"📊 Total de categorias: {categorias_count}")
    print(f"📊 Total de itens: {itens_count}")
    
    if categorias_count == 0:
        print("❌ Nenhuma categoria encontrada na base de dados!")
        return
    
    print("\n📋 Categorias encontradas:")
    print("-" * 40)
    
    categorias = CategoriaChecklist.objects.all().order_by('ordem')
    for categoria in categorias:
        itens_categoria = categoria.itens.count()
        print(f"  {categoria.ordem:2d}. {categoria.nome:<20} ({itens_categoria:2d} itens)")
    
    print("\n✅ Verificação concluída!")

if __name__ == '__main__':
    check_data()