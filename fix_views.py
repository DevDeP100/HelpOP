#!/usr/bin/env python3
"""
Script para corrigir o erro de categoria__ordem no arquivo views.py
"""

import re

# Ler o arquivo views.py
with open('core/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Substituir todas as ocorrências de categoria__ordem por ordem
# para itens_personalizados (que não têm categoria direta)
content = re.sub(
    r"checklist\.itens_personalizados\.filter\(ativo=True\)\.order_by\('categoria__ordem', 'ordem'\)",
    "checklist.itens_personalizados.filter(ativo=True).order_by('ordem')",
    content
)

# Escrever o arquivo corrigido
with open('core/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Arquivo views.py corrigido com sucesso!")
print("   - Removidas referências incorretas a categoria__ordem")
print("   - Mantida ordenação por ordem para itens_personalizados")
