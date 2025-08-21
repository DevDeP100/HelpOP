from rest_framework import serializers
from .models import (
    Usuario, Veiculo, Oficina, Profissional, Servico, Manutencao, Avaliacao,
    TipoVeiculo, CategoriaChecklist, ItemChecklist, Checklist, ItemChecklistPersonalizado,
    ChecklistExecutado, ItemChecklistExecutado, Arquivos_checklist, usuarioOficina
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

class ItemChecklistSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    
    class Meta:
        model = ItemChecklist
        fields = [
            'id', 'categoria', 'categoria_nome', 'nome', 'descricao',
            'tipo_verificacao', 'critico', 'ordem', 'ativo', 'data_criacao', 'data_atualizacao',
            'usuario', 'obrigatorio', 'created_by', 'updated_by'
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

class ItemChecklistPersonalizadoSerializer(serializers.ModelSerializer):
    checklist_nome = serializers.CharField(source='checklist.nome', read_only=True)
    item_padrao_nome = serializers.CharField(source='item_padrao.nome', read_only=True)
    item_nome = serializers.CharField(source='item_padrao.nome', read_only=True)
    
    class Meta:
        model = ItemChecklistPersonalizado
        fields = [
            'id', 'checklist', 'checklist_nome', 'item_padrao', 'item_padrao_nome', 'item_nome',
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
    item_checklist_nome = serializers.CharField(source='item_checklist.item_padrao.nome', read_only=True)
    
    class Meta:
        model = ItemChecklistExecutado
        fields = [
            'id', 'checklist_executado', 'checklist_executado_info',
            'item_checklist', 'item_checklist_nome', 'checked', 'resultado', 'observacoes',
            'data_criacao', 'data_atualizacao', 'created_by', 'updated_by'
        ]

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

class ChecklistExecutadoDetalhadoSerializer(serializers.ModelSerializer):
    checklist = ChecklistSerializer(read_only=True)
    veiculo = VeiculoSerializer(read_only=True)
    usuario = UsuarioSerializer(read_only=True)
    itens_executados = ItemChecklistExecutadoSerializer(many=True, read_only=True, source='checklist_executado')
    
    class Meta:
        model = ChecklistExecutado
        fields = [
            'id', 'checklist', 'veiculo', 'data_execucao', 'usuario',
            'observacoes', 'data_criacao', 'data_atualizacao', 'status', 'itens_executados', 'created_by', 'updated_by'
        ] 


class UsuarioOficinaSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.get_full_name', read_only=True)
    oficina_nome = serializers.CharField(source='oficina.nome', read_only=True)
    
    class Meta:
        model = usuarioOficina
        fields = [
            'id', 'usuario', 'usuario_nome', 'oficina', 'oficina_nome',
            'ativo', 'data_criacao', 'data_atualizacao', 'created_by', 'updated_by'
        ]
        read_only_fields = ['data_criacao', 'data_atualizacao']