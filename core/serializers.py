from rest_framework import serializers
from .models import (
    Usuario, Veiculo, Oficina, Profissional, Servico, Manutencao, Avaliacao,
    TipoVeiculo, CategoriaChecklist, ItemChecklist, Checklist, ItemChecklistPersonalizado,
    ChecklistExecutado, ItemChecklistExecutado, Arquivos_checklist, UsuarioOficina
)

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'telefone',
            'is_profissional', 'is_oficina', 'is_staff', 'is_active',
            'email_verificado', 'aprovado_pendente', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']

class VeiculoSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.get_full_name', read_only=True)
    created_by_nome = serializers.CharField(source='created_by.get_full_name', read_only=True)
    updated_by_nome = serializers.CharField(source='updated_by.get_full_name', read_only=True)
    
    class Meta:
        model = Veiculo
        fields = [
            'id', 'usuario', 'usuario_nome', 'marca', 'modelo', 'ano', 'placa', 'km_atual',
            'data_criacao', 'data_atualizacao', 'created_by', 'created_by_nome', 'updated_by', 'updated_by_nome'
        ]
        read_only_fields = ['data_criacao', 'data_atualizacao']

class OficinaSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.get_full_name', read_only=True)
    created_by_nome = serializers.CharField(source='created_by.get_full_name', read_only=True)
    updated_by_nome = serializers.CharField(source='updated_by.get_full_name', read_only=True)
    
    class Meta:
        model = Oficina
        fields = [
            'id', 'usuario', 'usuario_nome', 'nome', 'endereco', 'telefone',
            'email', 'site', 'cnpj', 'aprovado',
            'data_criacao', 'data_atualizacao', 'created_by', 'created_by_nome', 'updated_by', 'updated_by_nome'
        ]
        read_only_fields = ['data_criacao', 'data_atualizacao']

class ProfissionalSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.get_full_name', read_only=True)
    oficina_nome = serializers.CharField(source='oficina.nome', read_only=True)
    created_by_nome = serializers.CharField(source='created_by.get_full_name', read_only=True)
    updated_by_nome = serializers.CharField(source='updated_by.get_full_name', read_only=True)
    
    class Meta:
        model = Profissional
        fields = [
            'id', 'usuario', 'usuario_nome', 'especialidade', 'descricao',
            'aprovado', 'oficina', 'oficina_nome', 'cnpj', 'endereco',
            'data_criacao', 'data_atualizacao', 'created_by', 'created_by_nome', 'updated_by', 'updated_by_nome'
        ]
        read_only_fields = ['data_criacao', 'data_atualizacao']

class ServicoSerializer(serializers.ModelSerializer):
    created_by_nome = serializers.CharField(source='created_by.get_full_name', read_only=True)
    updated_by_nome = serializers.CharField(source='updated_by.get_full_name', read_only=True)
    class Meta:
        model = Servico
        fields = [
            'id', 'nome', 'descricao', 'preco_sugerido', 'ativo',
            'data_criacao', 'data_atualizacao', 'created_by', 'created_by_nome', 'updated_by', 'updated_by_nome'
        ]
        read_only_fields = ['data_criacao', 'data_atualizacao']

class ManutencaoSerializer(serializers.ModelSerializer):
    veiculo_info = serializers.CharField(source='veiculo.__str__', read_only=True)
    servico_nome = serializers.CharField(source='servico.nome', read_only=True)
    profissional_nome = serializers.CharField(source='profissional.usuario.get_full_name', read_only=True)
    created_by_nome = serializers.CharField(source='created_by.get_full_name', read_only=True)
    updated_by_nome = serializers.CharField(source='updated_by.get_full_name', read_only=True)
    
    class Meta:
        model = Manutencao
        fields = [
            'id', 'veiculo', 'veiculo_info', 'servico', 'servico_nome',
            'profissional', 'profissional_nome', 'data', 'km', 'valor', 'observacoes',
            'data_criacao', 'data_atualizacao', 'created_by', 'created_by_nome', 'updated_by', 'updated_by_nome'
        ]
        read_only_fields = ['data_criacao', 'data_atualizacao']

class AvaliacaoSerializer(serializers.ModelSerializer):
    profissional_nome = serializers.CharField(source='profissional.usuario.get_full_name', read_only=True)
    usuario_nome = serializers.CharField(source='usuario.get_full_name', read_only=True)
    
    class Meta:
        model = Avaliacao
        fields = [
            'id', 'profissional', 'profissional_nome', 'usuario', 'usuario_nome',
            'nota', 'comentario', 'data'
        ]
        read_only_fields = ['data']

# Serializers para o sistema de Checklist
class TipoVeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoVeiculo
        fields = ['id', 'nome', 'descricao', 'ativo', 'data_criacao', 'data_atualizacao', 'usuario', 'created_by', 'updated_by']
        read_only_fields = ['data_criacao', 'data_atualizacao']

class CategoriaChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaChecklist
        fields = ['id', 'nome', 'descricao', 'ordem', 'ativo', 'data_criacao', 'data_atualizacao', 'usuario', 'created_by', 'updated_by']
        read_only_fields = ['data_criacao', 'data_atualizacao']

class CategoriaChecklistDetalhadaSerializer(serializers.ModelSerializer):
    itens = serializers.SerializerMethodField()
    
    def get_itens(self, obj):
        return ItemChecklistSerializer(obj.itens.filter(ativo=True).order_by('ordem'), many=True, read_only=True).data
    
    class Meta:
        model = CategoriaChecklist
        fields = ['id', 'nome', 'descricao', 'ordem', 'ativo', 'data_criacao', 'data_atualizacao', 'usuario', 'itens', 'created_by', 'updated_by']
        read_only_fields = ['data_criacao', 'data_atualizacao']

class ItemChecklistSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    
    class Meta:
        model = ItemChecklist
        fields = [
            'id', 'categoria', 'categoria_nome', 'nome', 'descricao',
            'tipo_verificacao', 'critico', 'ordem', 'ativo', 'data_criacao', 'data_atualizacao',
            'usuario', 'obrigatorio', 'tipo_resultado', 'tipo_dado', 'created_by', 'updated_by'
        ]
        read_only_fields = ['data_criacao', 'data_atualizacao']

class ChecklistSerializer(serializers.ModelSerializer):
    oficina_nome = serializers.CharField(source='oficina.nome', read_only=True)
    tipo_veiculo_nome = serializers.CharField(source='tipo_veiculo.nome', read_only=True)
    created_by_nome = serializers.CharField(source='created_by.get_full_name', read_only=True)
    updated_by_nome = serializers.CharField(source='updated_by.get_full_name', read_only=True)
    
    class Meta:
        model = Checklist
        fields = [
            'id', 'oficina', 'oficina_nome', 'tipo_veiculo', 'tipo_veiculo_nome',
            'nome', 'descricao', 'ativo', 'data_criacao', 'data_atualizacao',
            'created_by', 'created_by_nome', 'updated_by', 'updated_by_nome'
        ]
        read_only_fields = ['data_criacao', 'data_atualizacao']

class ChecklistComItensAgrupadosSerializer(serializers.ModelSerializer):
    oficina = OficinaSerializer(read_only=True)
    tipo_veiculo = TipoVeiculoSerializer(read_only=True)
    itens_agrupados = serializers.SerializerMethodField()
    
    def get_itens_agrupados(self, obj):
        itens_personalizados = obj.itens_personalizados.filter(ativo=True).order_by('ordem')
        categorias_agrupadas = {}
        
        for item in itens_personalizados:
            if item.item_padrao and item.item_padrao.categoria:
                categoria_id = item.item_padrao.categoria.id
                if categoria_id not in categorias_agrupadas:
                    categorias_agrupadas[categoria_id] = {
                        'categoria': {
                            'id': item.item_padrao.categoria.id,
                            'nome': item.item_padrao.categoria.nome,
                            'descricao': item.item_padrao.categoria.descricao,
                            'ordem': item.item_padrao.categoria.ordem
                        },
                        'itens': []
                    }
                categorias_agrupadas[categoria_id]['itens'].append({
                    'id': item.id,
                    'ordem': item.ordem,
                    'critico': item.critico,
                    'obrigatorio': item.obrigatorio,
                    'item_padrao': {
                        'id': item.item_padrao.id,
                        'nome': item.item_padrao.nome,
                        'descricao': item.item_padrao.descricao,
                        'tipo_verificacao': item.item_padrao.tipo_verificacao
                    }
                })
        
        # Ordenar categorias pela ordem
        return sorted(categorias_agrupadas.values(), key=lambda x: x['categoria']['ordem'])
    
    class Meta:
        model = Checklist
        fields = [
            'id', 'oficina', 'tipo_veiculo', 'nome', 'descricao', 'ativo',
            'data_criacao', 'data_atualizacao', 'itens_agrupados', 'created_by', 'updated_by'
        ]
        read_only_fields = ['data_criacao', 'data_atualizacao']

class ItemChecklistPersonalizadoSerializer(serializers.ModelSerializer):
    checklist_nome = serializers.CharField(source='checklist.nome', read_only=True)
    item_padrao_nome = serializers.CharField(source='item_padrao.nome', read_only=True)
    item_padrao_info = serializers.SerializerMethodField()
    
    def get_item_padrao_info(self, obj):
        if obj.item_padrao:
            return {
                'id': obj.item_padrao.id,
                'nome': obj.item_padrao.nome,
                'descricao': obj.item_padrao.descricao,
                'tipo_verificacao': obj.item_padrao.tipo_verificacao,
                'categoria': {
                    'id': obj.item_padrao.categoria.id,
                    'nome': obj.item_padrao.categoria.nome
                }
            }
        return None
    
    class Meta:
        model = ItemChecklistPersonalizado
        fields = [
            'id', 'checklist', 'checklist_nome', 'item_padrao', 'item_padrao_nome', 'item_padrao_info',
            'critico', 'obrigatorio', 'ordem', 'ativo', 'data_criacao', 'data_atualizacao', 'created_by', 'updated_by'
        ]
        read_only_fields = ['data_criacao', 'data_atualizacao']

class ChecklistExecutadoSerializer(serializers.ModelSerializer):
    checklist_nome = serializers.CharField(source='checklist.nome', read_only=True)
    veiculo_info = serializers.CharField(source='veiculo.__str__', read_only=True)
    usuario_nome = serializers.CharField(source='usuario.get_full_name', read_only=True)
    created_by_nome = serializers.CharField(source='created_by.get_full_name', read_only=True)
    updated_by_nome = serializers.CharField(source='updated_by.get_full_name', read_only=True)
    
    class Meta:
        model = ChecklistExecutado
        fields = [
            'id', 'checklist', 'checklist_nome', 'veiculo', 'veiculo_info',
            'data_execucao', 'usuario', 'usuario_nome', 'observacoes',
            'status', 'data_criacao', 'data_atualizacao', 'created_by', 'created_by_nome', 'updated_by', 'updated_by_nome'
        ]
        read_only_fields = ['data_execucao', 'data_criacao', 'data_atualizacao']

class ItemChecklistExecutadoSerializer(serializers.ModelSerializer):
    checklist_executado_info = serializers.CharField(source='checklist_executado.__str__', read_only=True)
    item_checklist_info = serializers.SerializerMethodField()
    
    def get_item_checklist_info(self, obj):
        if obj.item_checklist:
            return {
                'id': obj.item_checklist.id,
                'ordem': obj.item_checklist.ordem,
                'critico': obj.item_checklist.critico,
                'obrigatorio': obj.item_checklist.obrigatorio,
                'item_padrao': {
                    'id': obj.item_checklist.item_padrao.id,
                    'nome': obj.item_checklist.item_padrao.nome,
                    'descricao': obj.item_checklist.item_padrao.descricao,
                    'tipo_verificacao': obj.item_checklist.item_padrao.tipo_verificacao,
                    'categoria': {
                        'id': obj.item_checklist.item_padrao.categoria.id,
                        'nome': obj.item_checklist.item_padrao.categoria.nome
                    }
                } if obj.item_checklist.item_padrao else None
            }
        return None
    
    class Meta:
        model = ItemChecklistExecutado
        fields = [
            'id', 'checklist_executado', 'checklist_executado_info',
            'item_checklist', 'item_checklist_info', 'resultado', 'valor_resultado', 'observacoes',
            'data_criacao', 'data_atualizacao', 'created_by', 'updated_by'
        ]
        read_only_fields = ['data_criacao', 'data_atualizacao']

class ArquivosChecklistSerializer(serializers.ModelSerializer):
    item_checklist_executado_info = serializers.CharField(source='item_checklist_executado.__str__', read_only=True)
    
    class Meta:
        model = Arquivos_checklist
        fields = [
            'id', 'item_checklist_executado', 'item_checklist_executado_info',
            'arquivo', 'tipo', 'data_criacao', 'data_atualizacao', 'created_by', 'updated_by'
        ]

# Serializers para listas detalhadas
class ChecklistDetalhadoSerializer(serializers.ModelSerializer):
    oficina = OficinaSerializer(read_only=True)
    tipo_veiculo = TipoVeiculoSerializer(read_only=True)
    itens_personalizados = ItemChecklistPersonalizadoSerializer(many=True, read_only=True)
    execucoes = ChecklistExecutadoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Checklist
        fields = [
            'id', 'oficina', 'tipo_veiculo', 'nome', 'descricao', 'ativo',
            'data_criacao', 'data_atualizacao', 'created_by', 'updated_by',
            'itens_personalizados', 'execucoes'
        ]
        read_only_fields = ['data_criacao', 'data_atualizacao']

class ChecklistExecutadoDetalhadoSerializer(serializers.ModelSerializer):
    checklist = ChecklistSerializer(read_only=True)
    veiculo = VeiculoSerializer(read_only=True)
    usuario = UsuarioSerializer(read_only=True)
    itens_executados = ItemChecklistExecutadoSerializer(many=True, read_only=True, source='itens_executados')
    
    class Meta:
        model = ChecklistExecutado
        fields = [
            'id', 'checklist', 'veiculo', 'data_execucao', 'usuario',
            'observacoes', 'data_criacao', 'data_atualizacao', 'status', 'itens_executados', 'created_by', 'updated_by'
        ]
        read_only_fields = ['data_execucao', 'data_criacao', 'data_atualizacao']

class ChecklistExecutadoComItensAgrupadosSerializer(serializers.ModelSerializer):
    checklist = ChecklistSerializer(read_only=True)
    veiculo = VeiculoSerializer(read_only=True)
    usuario = UsuarioSerializer(read_only=True)
    itens_agrupados = serializers.SerializerMethodField()
    
    def get_itens_agrupados(self, obj):
        itens_executados = obj.itens_executados.all().order_by('item_checklist__ordem')
        categorias_agrupadas = {}
        
        for item_executado in itens_executados:
            if item_executado.item_checklist.item_padrao and item_executado.item_checklist.item_padrao.categoria:
                categoria_id = item_executado.item_checklist.item_padrao.categoria.id
                if categoria_id not in categorias_agrupadas:
                    categorias_agrupadas[categoria_id] = {
                        'categoria': {
                            'id': item_executado.item_checklist.item_padrao.categoria.id,
                            'nome': item_executado.item_checklist.item_padrao.categoria.nome,
                            'descricao': item_executado.item_checklist.item_padrao.categoria.descricao,
                            'ordem': item_executado.item_checklist.item_padrao.categoria.ordem
                        },
                        'itens': []
                    }
                categorias_agrupadas[categoria_id]['itens'].append({
                    'id': item_executado.id,
                    'ordem': item_executado.item_checklist.ordem,
                    'critico': item_executado.item_checklist.critico,
                    'obrigatorio': item_executado.item_checklist.obrigatorio,
                    'resultado': item_executado.resultado,
                    'valor_resultado': item_executado.valor_resultado,
                    'observacoes': item_executado.observacoes,
                    'item_padrao': {
                        'id': item_executado.item_checklist.item_padrao.id,
                        'nome': item_executado.item_checklist.item_padrao.nome,
                        'descricao': item_executado.item_checklist.item_padrao.descricao,
                        'tipo_verificacao': item_executado.item_checklist.item_padrao.tipo_verificacao
                    }
                })
        
        # Ordenar categorias pela ordem
        return sorted(categorias_agrupadas.values(), key=lambda x: x['categoria']['ordem'])
    
    class Meta:
        model = ChecklistExecutado
        fields = [
            'id', 'checklist', 'veiculo', 'data_execucao', 'usuario',
            'observacoes', 'data_criacao', 'data_atualizacao', 'status', 'itens_agrupados', 'created_by', 'updated_by'
        ]
        read_only_fields = ['data_execucao', 'data_criacao', 'data_atualizacao']

class UsuarioOficinaSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.get_full_name', read_only=True)
    oficina_nome = serializers.CharField(source='oficina.nome', read_only=True)
    
    class Meta:
        model = UsuarioOficina
        fields = [
            'id', 'usuario', 'usuario_nome', 'oficina', 'oficina_nome',
            'ativo', 'data_criacao', 'data_atualizacao', 'created_by', 'updated_by'
        ]
        read_only_fields = ['data_criacao', 'data_atualizacao']