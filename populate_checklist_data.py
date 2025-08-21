#!/usr/bin/env python
"""
Script para popular a base de dados com categorias e itens de checklist automotivo
Base de dados: PostgreSQL na nuvem (Railway)
"""

import os
import sys
import django
import psycopg2
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpOP.settings')
django.setup()

from core.models import CategoriaChecklist, ItemChecklist, Usuario

# Dados das categorias e itens de checklist automotivo
CHECKLIST_DATA = {
    "Motor": {
        "descricao": "Verificações relacionadas ao motor e sistema de combustão",
        "ordem": 1,
        "itens": [
            "Verificar nível de óleo do motor",
            "Verificar cor e consistência do óleo",
            "Verificar vazamentos de óleo",
            "Verificar nível do líquido de arrefecimento",
            "Verificar estado das mangueiras do radiador",
            "Verificar funcionamento do ventilador",
            "Verificar correia do alternador",
            "Verificar correia da direção hidráulica",
            "Verificar correia do ar condicionado",
            "Verificar filtro de ar",
            "Verificar velas de ignição",
            "Verificar cabos de vela",
            "Verificar bateria e terminais",
            "Verificar funcionamento do motor de partida",
            "Verificar alternador",
            "Verificar sistema de escape",
            "Verificar catalisador",
            "Verificar sensor de oxigênio",
            "Verificar sistema de injeção eletrônica",
            "Verificar filtro de combustível"
        ]
    },
    "Freios": {
        "descricao": "Sistema de frenagem e componentes relacionados",
        "ordem": 2,
        "itens": [
            "Verificar nível do fluido de freio",
            "Verificar cor do fluido de freio",
            "Verificar vazamentos no sistema",
            "Verificar espessura das pastilhas dianteiras",
            "Verificar espessura das pastilhas traseiras",
            "Verificar estado dos discos de freio",
            "Verificar funcionamento do freio de mão",
            "Verificar cabo do freio de mão",
            "Verificar cilindro mestre",
            "Verificar servo freio",
            "Verificar mangueiras de freio",
            "Verificar ABS (se equipado)",
            "Verificar pedal de freio",
            "Verificar luz de freio",
            "Verificar regulagem do freio traseiro"
        ]
    },
    "Suspensão": {
        "descricao": "Sistema de suspensão e direção",
        "ordem": 3,
        "itens": [
            "Verificar amortecedores dianteiros",
            "Verificar amortecedores traseiros",
            "Verificar molas dianteiras",
            "Verificar molas traseiras",
            "Verificar buchas da suspensão",
            "Verificar pivôs da suspensão",
            "Verificar barra estabilizadora",
            "Verificar coxins do amortecedor",
            "Verificar batentes da suspensão",
            "Verificar coifas da suspensão",
            "Verificar alinhamento das rodas",
            "Verificar balanceamento das rodas",
            "Verificar geometria da suspensão",
            "Verificar folgas na direção",
            "Verificar funcionamento da direção hidráulica"
        ]
    },
    "Direção": {
        "descricao": "Sistema de direção e componentes",
        "ordem": 4,
        "itens": [
            "Verificar fluido da direção hidráulica",
            "Verificar vazamentos na direção",
            "Verificar bomba da direção hidráulica",
            "Verificar mangueiras da direção",
            "Verificar caixa de direção",
            "Verificar terminais de direção",
            "Verificar rotulas da direção",
            "Verificar coifas da direção",
            "Verificar volante",
            "Verificar coluna de direção",
            "Verificar funcionamento da direção elétrica (se equipado)",
            "Verificar sensor de direção (se equipado)",
            "Verificar assistência da direção"
        ]
    },
    "Pneus e Rodas": {
        "descricao": "Pneus, rodas e componentes relacionados",
        "ordem": 5,
        "itens": [
            "Verificar pressão dos pneus",
            "Verificar desgaste dos pneus dianteiros",
            "Verificar desgaste dos pneus traseiros",
            "Verificar desgaste irregular dos pneus",
            "Verificar profundidade do sulco",
            "Verificar estado das rodas",
            "Verificar porcas das rodas",
            "Verificar estepe",
            "Verificar macaco",
            "Verificar chave de roda",
            "Verificar válvulas dos pneus",
            "Verificar balanceamento",
            "Verificar alinhamento",
            "Verificar calibragem"
        ]
    },
    "Transmissão": {
        "descricao": "Sistema de transmissão e embreagem",
        "ordem": 6,
        "itens": [
            "Verificar óleo da transmissão",
            "Verificar vazamentos na transmissão",
            "Verificar funcionamento da embreagem",
            "Verificar fluido da embreagem",
            "Verificar cabo da embreagem",
            "Verificar pedal da embreagem",
            "Verificar homocinéticas",
            "Verificar coifas das homocinéticas",
            "Verificar semieixos",
            "Verificar diferencial",
            "Verificar óleo do diferencial",
            "Verificar funcionamento do câmbio",
            "Verificar sincronizadores",
            "Verificar alavanca do câmbio"
        ]
    },
    "Elétrica": {
        "descricao": "Sistema elétrico e eletrônico",
        "ordem": 7,
        "itens": [
            "Verificar bateria",
            "Verificar alternador",
            "Verificar motor de partida",
            "Verificar fusíveis",
            "Verificar relés",
            "Verificar chicote elétrico",
            "Verificar faróis dianteiros",
            "Verificar lanternas traseiras",
            "Verificar pisca-pisca",
            "Verificar luz de freio",
            "Verificar luz de ré",
            "Verificar luz de placa",
            "Verificar farol de neblina",
            "Verificar buzina",
            "Verificar limpador de para-brisa",
            "Verificar lavador de para-brisa",
            "Verificar ar condicionado",
            "Verificar aquecedor",
            "Verificar rádio",
            "Verificar sistema de alarme",
            "Verificar travas elétricas",
            "Verificar vidros elétricos"
        ]
    },
    "Carroceria": {
        "descricao": "Estrutura da carroceria e componentes externos",
        "ordem": 8,
        "itens": [
            "Verificar estado da pintura",
            "Verificar riscos na pintura",
            "Verificar amassados na lataria",
            "Verificar corrosão/ferrugem",
            "Verificar para-choques",
            "Verificar para-lamas",
            "Verificar portas",
            "Verificar fechaduras das portas",
            "Verificar dobradiças das portas",
            "Verificar vidros",
            "Verificar para-brisa",
            "Verificar vidro traseiro",
            "Verificar espelhos retrovisores",
            "Verificar antena",
            "Verificar teto solar (se equipado)",
            "Verificar bagageiro",
            "Verificar capô",
            "Verificar tampa do porta-malas"
        ]
    },
    "Interior": {
        "descricao": "Componentes internos do veículo",
        "ordem": 9,
        "itens": [
            "Verificar bancos dianteiros",
            "Verificar bancos traseiros",
            "Verificar cintos de segurança",
            "Verificar painel de instrumentos",
            "Verificar velocímetro",
            "Verificar hodômetro",
            "Verificar indicador de combustível",
            "Verificar indicador de temperatura",
            "Verificar luzes de advertência",
            "Verificar ar condicionado",
            "Verificar aquecedor",
            "Verificar ventilação",
            "Verificar rádio/som",
            "Verificar porta-luvas",
            "Verificar console central",
            "Verificar tapetes",
            "Verificar forração do teto",
            "Verificar apoios de cabeça",
            "Verificar apoios de braço"
        ]
    },
    "Segurança": {
        "descricao": "Itens de segurança obrigatórios e opcionais",
        "ordem": 10,
        "itens": [
            "Verificar triângulo de segurança",
            "Verificar extintor de incêndio",
            "Verificar kit de primeiros socorros",
            "Verificar chave de roda",
            "Verificar macaco",
            "Verificar estepe",
            "Verificar cintos de segurança",
            "Verificar airbags (se equipado)",
            "Verificar travas de segurança",
            "Verificar alarme",
            "Verificar sistema antifurto",
            "Verificar documentação do veículo",
            "Verificar CRLV",
            "Verificar seguro obrigatório",
            "Verificar licenciamento"
        ]
    }
}

def create_admin_user():
    """Criar usuário administrador se não existir"""
    try:
        admin_user = Usuario.objects.filter(is_staff=True).first()
        if not admin_user:
            admin_user = Usuario.objects.create_user(
                username='admin_checklist',
                email='admin@helpop.com.br',
                password='admin123',
                is_staff=True,
                is_superuser=True,
                email_verificado=True
            )
            print(f"Usuário administrador criado: {admin_user.username}")
        return admin_user
    except Exception as e:
        print(f"Erro ao criar usuário administrador: {e}")
        return None

def populate_checklist_data():
    """Popular as tabelas com dados de checklist automotivo"""
    try:
        # Criar usuário administrador
        admin_user = create_admin_user()
        if not admin_user:
            print("Erro: Não foi possível criar usuário administrador")
            return False

        print("Iniciando população dos dados de checklist...")
        
        # Limpar dados existentes (opcional)
        print("Limpando dados existentes...")
        ItemChecklist.objects.all().delete()
        CategoriaChecklist.objects.all().delete()
        
        categorias_criadas = 0
        itens_criados = 0
        
        # Criar categorias e itens
        for categoria_nome, categoria_data in CHECKLIST_DATA.items():
            print(f"Criando categoria: {categoria_nome}")
            
            # Criar categoria
            categoria = CategoriaChecklist.objects.create(
                nome=categoria_nome,
                descricao=categoria_data['descricao'],
                ordem=categoria_data['ordem'],
                ativo=True,
                usuario=admin_user,
                created_by=admin_user,
                updated_by=admin_user
            )
            categorias_criadas += 1
            
            # Criar itens da categoria
            for ordem, item_nome in enumerate(categoria_data['itens'], 1):
                ItemChecklist.objects.create(
                    categoria=categoria,
                    nome=item_nome,
                    descricao=f"Verificação: {item_nome}",
                    ordem=ordem,
                    obrigatorio=True,
                    ativo=True,
                    usuario=admin_user,
                    created_by=admin_user,
                    updated_by=admin_user
                )
                itens_criados += 1
            
            print(f"  - {len(categoria_data['itens'])} itens criados")
        
        print(f"\n✅ População concluída com sucesso!")
        print(f"📊 Estatísticas:")
        print(f"   - Categorias criadas: {categorias_criadas}")
        print(f"   - Itens criados: {itens_criados}")
        print(f"   - Total de verificações: {itens_criados}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante a população: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_data():
    """Verificar os dados criados"""
    try:
        print("\n🔍 Verificando dados criados...")
        
        categorias = CategoriaChecklist.objects.all().order_by('ordem')
        print(f"\nCategorias encontradas: {categorias.count()}")
        
        for categoria in categorias:
            itens_count = ItemChecklist.objects.filter(categoria=categoria).count()
            print(f"  - {categoria.nome}: {itens_count} itens")
        
        total_itens = ItemChecklist.objects.count()
        print(f"\nTotal de itens de checklist: {total_itens}")
        
    except Exception as e:
        print(f"Erro ao verificar dados: {e}")

if __name__ == '__main__':
    print("🚗 Script de População de Checklist Automotivo - HelpOP")
    print("=" * 60)
    
    # Verificar conexão com banco
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("✅ Conexão com banco de dados estabelecida")
    except Exception as e:
        print(f"❌ Erro de conexão com banco: {e}")
        sys.exit(1)
    
    # Popular dados
    if populate_checklist_data():
        verify_data()
        print("\n🎉 Script executado com sucesso!")
    else:
        print("\n❌ Falha na execução do script")
        sys.exit(1)