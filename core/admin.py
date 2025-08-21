from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, Veiculo, Profissional, Servico, Manutencao, Avaliacao,
    TipoVeiculo, CategoriaChecklist, ItemChecklist, Checklist, ItemChecklistPersonalizado,
    ChecklistExecutado, ItemChecklistExecutado, Arquivos_checklist, Oficina, usuarioOficina
)

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_profissional', 'is_staff', 'is_active')
    list_filter = ('is_profissional', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('telefone', 'is_profissional')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {'fields': ('telefone', 'is_profissional')}),
    )

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'ano', 'placa', 'km_atual', 'usuario')
    list_filter = ('marca', 'ano', 'usuario')
    search_fields = ('marca', 'modelo', 'placa', 'usuario__username')
    ordering = ('marca', 'modelo')

@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'especialidade', 'aprovado', 'data_cadastro')
    list_filter = ('especialidade', 'aprovado')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name', 'especialidade')
    ordering = ('usuario__username',)
    
    def data_cadastro(self, obj):
        return obj.usuario.date_joined.strftime('%d/%m/%Y')
    data_cadastro.short_description = 'Data de Cadastro'

@admin.register(Oficina)
class OficinaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario', 'aprovado', 'cnpj')
    list_filter = ('aprovado',)
    search_fields = ('nome', 'usuario__username', 'cnpj', 'email')
    ordering = ('nome',)

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco_sugerido', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome', 'descricao')
    ordering = ('nome',)

@admin.register(Manutencao)
class ManutencaoAdmin(admin.ModelAdmin):
    list_display = ('veiculo', 'servico', 'data', 'km', 'valor', 'profissional')
    list_filter = ('data', 'servico', 'profissional')
    search_fields = ('veiculo__marca', 'veiculo__modelo', 'servico__nome')
    ordering = ('-data',)
    date_hierarchy = 'data'

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('profissional', 'usuario', 'nota', 'data')
    list_filter = ('nota', 'data', 'profissional')
    search_fields = ('profissional__usuario__username', 'usuario__username')
    ordering = ('-data',)
    date_hierarchy = 'data'

# Admin para os novos models de Checklist
@admin.register(TipoVeiculo)
class TipoVeiculoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo', 'data_criacao')
    list_filter = ('ativo', 'data_criacao')
    search_fields = ('nome', 'descricao')
    ordering = ('nome',)

@admin.register(CategoriaChecklist)
class CategoriaChecklistAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ordem', 'ativo', 'data_criacao')
    list_filter = ('ativo', 'data_criacao')
    search_fields = ('nome', 'descricao')
    ordering = ('ordem', 'nome')
    list_editable = ('ordem', 'ativo')

@admin.register(ItemChecklist)
class ItemChecklistAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'tipo_verificacao', 'critico', 'ordem', 'ativo')
    list_filter = ('categoria', 'tipo_verificacao', 'critico', 'ativo', 'data_criacao')
    search_fields = ('nome', 'descricao', 'categoria__nome')
    ordering = ('categoria__ordem', 'ordem', 'nome')
    list_editable = ('ordem', 'ativo', 'critico')

@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('nome', 'oficina', 'tipo_veiculo', 'ativo', 'data_criacao')
    list_filter = ('oficina', 'tipo_veiculo', 'ativo', 'data_criacao')
    search_fields = ('nome', 'descricao', 'oficina__nome', 'tipo_veiculo__nome')
    ordering = ('oficina__nome', 'tipo_veiculo__nome', 'nome')
    list_editable = ('ativo',)

@admin.register(ItemChecklistPersonalizado)
class ItemChecklistPersonalizadoAdmin(admin.ModelAdmin):
    list_display = ('checklist', 'critico', 'obrigatorio', 'ordem', 'ativo')
    list_filter = ('checklist', 'critico', 'obrigatorio', 'ativo', 'data_criacao')
    search_fields = ('descricao', 'checklist__nome')
    ordering = ('checklist',)
    list_editable = ('ativo', 'critico', 'obrigatorio')

@admin.register(ChecklistExecutado)
class ChecklistExecutadoAdmin(admin.ModelAdmin):
    list_display = ('checklist', 'get_veiculo_display', 'usuario', 'data_execucao', 'status', 'data_atualizacao')
    list_filter = ('status', 'data_execucao', 'checklist__oficina', 'checklist__tipo_veiculo', 'veiculo__marca')
    search_fields = ('checklist__nome', 'usuario__username', 'veiculo__placa', 'veiculo__marca', 'observacoes')
    ordering = ('-data_execucao',)
    date_hierarchy = 'data_execucao'
    
    def get_veiculo_display(self, obj):
        if obj.veiculo:
            return f"{obj.veiculo.marca} {obj.veiculo.modelo} ({obj.veiculo.placa})"
        return "Não especificado"
    get_veiculo_display.short_description = 'Veículo'

@admin.register(ItemChecklistExecutado)
class ItemChecklistExecutadoAdmin(admin.ModelAdmin):
    list_display = ('checklist_executado', 'item_checklist', 'checked', 'resultado', 'data_criacao', 'data_atualizacao')    
    list_filter = ('checked', 'resultado', 'item_checklist')
    search_fields = ('item_checklist__nome', 'observacoes')
    ordering = ('checklist_executado', 'item_checklist__ordem')

@admin.register(Arquivos_checklist)
class ArquivosChecklistAdmin(admin.ModelAdmin):
    list_display = ('item_checklist_executado', 'arquivo', 'tipo', 'data_criacao', 'data_atualizacao')
    list_filter = ('tipo', 'item_checklist_executado')
    search_fields = ('arquivo', 'item_checklist_executado')
    ordering = ('item_checklist_executado', 'arquivo')

@admin.register(usuarioOficina)
class usuarioOficinaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'oficina', 'ativo', 'data_criacao', 'data_atualizacao')
    list_filter = ('ativo', 'data_criacao', 'data_atualizacao')
    search_fields = ('usuario__username', 'oficina__nome')
    ordering = ('usuario', 'oficina')
