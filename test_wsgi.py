#!/usr/bin/env python3
"""
Teste do WSGI para verificar se está funcionando corretamente
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

print(f"📁 Diretório raiz: {project_root}")
print(f"📁 Python path: {sys.path[:3]}")

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpOP.settings')
    print("✅ DJANGO_SETTINGS_MODULE configurado")
    
    from django.core.wsgi import get_wsgi_application
    print("✅ Django WSGI importado")
    
    application = get_wsgi_application()
    print("✅ Aplicação WSGI criada com sucesso")
    
    print("🎉 WSGI está funcionando corretamente!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc() 