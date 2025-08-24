import os
import django
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpOP.settings')
django.setup()

from core.models import CategoriaChecklist, ItemChecklist

def export_to_remote_db():
    """
    Exporta dados das tabelas categorias_checklist e itens_checklist
    da base local para a base PostgreSQL remota
    """
    
    # Configuração da base remota
    remote_db_config = {
        'host': 'trolley.proxy.rlwy.net',
        'port': 14948,
        'database': 'railway',
        'user': 'postgres',
        'password': 'KHNuDctoBYMCxnEHuxyaiPEUFHYEVWFr'
    }
    
    try:
        # Conectar à base remota
        print("Conectando à base de dados remota...")
        remote_conn = psycopg2.connect(**remote_db_config)
        remote_cursor = remote_conn.cursor(cursor_factory=RealDictCursor)
        
        # Exportar CategoriaChecklist
        print("\nExportando categorias...")
        categorias = CategoriaChecklist.objects.all().order_by('id')
        categorias_exportadas = 0
        
        for categoria in categorias:
            # Verificar se já existe
            remote_cursor.execute(
                "SELECT id FROM categorias_checklist WHERE id = %s",
                (categoria.id,)
            )
            exists = remote_cursor.fetchone()
            
            if exists:
                # Atualizar registro existente
                update_query = """
                    UPDATE categorias_checklist SET
                        nome = %s,
                        descricao = %s,
                        ordem = %s,
                        ativo = %s,
                        data_criacao = %s,
                        usuario_id = %s,
                        data_atualizacao = %s,
                        created_by_id = %s,
                        updated_by_id = %s
                    WHERE id = %s
                """
                remote_cursor.execute(update_query, (
                    categoria.nome,
                    categoria.descricao,
                    categoria.ordem,
                    categoria.ativo,
                    categoria.data_criacao,
                    categoria.usuario_id,
                    categoria.data_atualizacao,
                    categoria.created_by_id,
                    categoria.updated_by_id,
                    categoria.id
                ))
                print(f"  Categoria atualizada: {categoria.nome} (ID: {categoria.id})")
            else:
                # Inserir novo registro
                insert_query = """
                    INSERT INTO categorias_checklist (
                        id, nome, descricao, ordem, ativo, data_criacao,
                        usuario_id, data_atualizacao, created_by_id, updated_by_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                remote_cursor.execute(insert_query, (
                    categoria.id,
                    categoria.nome,
                    categoria.descricao,
                    categoria.ordem,
                    categoria.ativo,
                    categoria.data_criacao,
                    categoria.usuario_id,
                    categoria.data_atualizacao,
                    categoria.created_by_id,
                    categoria.updated_by_id
                ))
                print(f"  Categoria inserida: {categoria.nome} (ID: {categoria.id})")
            
            categorias_exportadas += 1
        
        # Exportar ItemChecklist
        print("\nExportando itens do checklist...")
        itens = ItemChecklist.objects.all().order_by('id')
        itens_exportados = 0
        
        for item in itens:
            # Verificar se já existe
            remote_cursor.execute(
                "SELECT id FROM itens_checklist WHERE id = %s",
                (item.id,)
            )
            exists = remote_cursor.fetchone()
            
            if exists:
                # Atualizar registro existente
                update_query = """
                    UPDATE itens_checklist SET
                        categoria_id = %s,
                        nome = %s,
                        descricao = %s,
                        tipo_verificacao = %s,
                        critico = %s,
                        ordem = %s,
                        ativo = %s,
                        data_criacao = %s,
                        tipo_resultado = %s,
                        tipo_dado = %s,
                        usuario_id = %s,
                        obrigatorio = %s,
                        data_atualizacao = %s,
                        created_by_id = %s,
                        updated_by_id = %s
                    WHERE id = %s
                """
                remote_cursor.execute(update_query, (
                    item.categoria_id,
                    item.nome,
                    item.descricao,
                    item.tipo_verificacao,
                    item.critico,
                    item.ordem,
                    item.ativo,
                    item.data_criacao,
                    item.tipo_resultado,
                    item.tipo_dado,
                    item.usuario_id,
                    item.obrigatorio,
                    item.data_atualizacao,
                    item.created_by_id,
                    item.updated_by_id,
                    item.id
                ))
                print(f"  Item atualizado: {item.nome} (ID: {item.id})")
            else:
                # Inserir novo registro
                insert_query = """
                    INSERT INTO itens_checklist (
                        id, categoria_id, nome, descricao, tipo_verificacao,
                        critico, ordem, ativo, data_criacao, tipo_resultado,
                        tipo_dado, usuario_id, obrigatorio, data_atualizacao,
                        created_by_id, updated_by_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                remote_cursor.execute(insert_query, (
                    item.id,
                    item.categoria_id,
                    item.nome,
                    item.descricao,
                    item.tipo_verificacao,
                    item.critico,
                    item.ordem,
                    item.ativo,
                    item.data_criacao,
                    item.tipo_resultado,
                    item.tipo_dado,
                    item.usuario_id,
                    item.obrigatorio,
                    item.data_atualizacao,
                    item.created_by_id,
                    item.updated_by_id
                ))
                print(f"  Item inserido: {item.nome} (ID: {item.id})")
            
            itens_exportados += 1
        
        # Confirmar transações
        remote_conn.commit()
        
        print(f"\n✅ Exportação concluída com sucesso!")
        print(f"📊 Categorias exportadas: {categorias_exportadas}")
        print(f"📋 Itens exportados: {itens_exportados}")
        
    except psycopg2.Error as e:
        print(f"❌ Erro na base de dados: {e}")
        if 'remote_conn' in locals():
            remote_conn.rollback()
    except Exception as e:
        print(f"❌ Erro geral: {e}")
    finally:
        if 'remote_cursor' in locals():
            remote_cursor.close()
        if 'remote_conn' in locals():
            remote_conn.close()
            print("\n🔌 Conexão com a base remota fechada.")

def export_to_json():
    """
    Exporta dados para arquivos JSON como backup
    """
    print("\nCriando backup em JSON...")
    
    # Exportar categorias
    categorias_data = []
    for categoria in CategoriaChecklist.objects.all():
        categorias_data.append({
            'id': categoria.id,
            'nome': categoria.nome,
            'descricao': categoria.descricao,
            'ordem': categoria.ordem,
            'ativo': categoria.ativo,
            'data_criacao': categoria.data_criacao.isoformat(),
            'usuario_id': categoria.usuario_id,
            'data_atualizacao': categoria.data_atualizacao.isoformat(),
            'created_by_id': categoria.created_by_id,
            'updated_by_id': categoria.updated_by_id
        })
    
    # Exportar itens
    itens_data = []
    for item in ItemChecklist.objects.all():
        itens_data.append({
            'id': item.id,
            'categoria_id': item.categoria_id,
            'nome': item.nome,
            'descricao': item.descricao,
            'tipo_verificacao': item.tipo_verificacao,
            'critico': item.critico,
            'ordem': item.ordem,
            'ativo': item.ativo,
            'data_criacao': item.data_criacao.isoformat(),
            'tipo_resultado': item.tipo_resultado,
            'tipo_dado': item.tipo_dado,
            'usuario_id': item.usuario_id,
            'obrigatorio': item.obrigatorio,
            'data_atualizacao': item.data_atualizacao.isoformat(),
            'created_by_id': item.created_by_id,
            'updated_by_id': item.updated_by_id
        })
    
    # Salvar arquivos JSON
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    with open(f'backup_categorias_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(categorias_data, f, ensure_ascii=False, indent=2)
    
    with open(f'backup_itens_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(itens_data, f, ensure_ascii=False, indent=2)
    
    print(f"📁 Backup criado: backup_categorias_{timestamp}.json")
    print(f"📁 Backup criado: backup_itens_{timestamp}.json")

if __name__ == '__main__':
    print("🚀 Iniciando exportação de dados do checklist...")
    print("="*50)
    
    # Criar backup em JSON primeiro
    export_to_json()
    
    # Exportar para base remota
    export_to_remote_db()
    
    print("\n" + "="*50)
    print("✨ Processo de exportação finalizado!")