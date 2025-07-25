from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Veiculo, Profissional, Servico, Manutencao, Avaliacao

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
