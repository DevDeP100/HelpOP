from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from .models import (
    Usuario, Veiculo, Profissional, Servico, Manutencao, Avaliacao,
    TipoVeiculo, CategoriaChecklist, ItemChecklist, Checklist, ItemChecklistPersonalizado,
    ChecklistExecutado, ItemChecklistExecutado, Arquivos_checklist, Oficina, usuarioOficina
)
from .email_utils import enviar_email_aprovacao, enviar_email_rejeicao

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_profissional', 'is_oficina', 'email_verificado', 'aprovado_pendente', 'is_staff', 'is_active')
    list_filter = ('is_profissional', 'is_oficina', 'email_verificado', 'aprovado_pendente', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    actions = ['aprovar_usuarios', 'rejeitar_usuarios']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('telefone', 'is_profissional', 'is_oficina', 'email_verificado', 'aprovado_pendente')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {'fields': ('telefone', 'is_profissional', 'is_oficina')}),
    )
    
    def aprovar_usuarios(self, request, queryset):
        """Aprovar usuários selecionados"""
        aprovados = 0
        emails_enviados = 0
        
        for usuario in queryset:
            if (usuario.is_profissional or usuario.is_oficina) and usuario.aprovado_pendente and usuario.email_verificado:
                # Aprovar usuário
                usuario.aprovado_pendente = False
                usuario.save()
                aprovados += 1
                
                # Enviar email de aprovação
                try:
                    if enviar_email_aprovacao(usuario):
                        emails_enviados += 1
                        try:
                            self.message_user(request, f'✅ {usuario.username} aprovado e email enviado para {usuario.email}', level=messages.SUCCESS)
                        except:
                            pass  # Ignorar erros de mensagens
                    else:
                        try:
                            self.message_user(request, f'⚠️ {usuario.username} aprovado, mas falha no envio do email para {usuario.email}', level=messages.WARNING)
                        except:
                            pass  # Ignorar erros de mensagens
                except Exception as e:
                    try:
                        self.message_user(request, f'❌ Erro ao enviar email para {usuario.username}: {str(e)}', level=messages.ERROR)
                    except:
                        pass  # Ignorar erros de mensagens
            else:
                # Explicar por que não foi aprovado
                motivos = []
                if not (usuario.is_profissional or usuario.is_oficina):
                    motivos.append("não é profissional/oficina")
                if not usuario.aprovado_pendente:
                    motivos.append("não está pendente")
                if not usuario.email_verificado:
                    motivos.append("email não verificado")
                
                try:
                    self.message_user(request, f'⏭️ {usuario.username} não foi aprovado: {", ".join(motivos)}', level=messages.INFO)
                except:
                    pass  # Ignorar erros de mensagens
        
        # Resumo final
        if aprovados > 0:
            try:
                self.message_user(request, f'🎉 APROVAÇÃO CONCLUÍDA: {aprovados} usuário(s) aprovado(s), {emails_enviados} email(s) enviado(s)', level=messages.SUCCESS)
            except:
                pass  # Ignorar erros de mensagens
        else:
            try:
                self.message_user(request, '⚠️ Nenhum usuário foi aprovado. Verifique os critérios de seleção.', level=messages.WARNING)
            except:
                pass  # Ignorar erros de mensagens
    
    aprovar_usuarios.short_description = "Aprovar usuários selecionados"
    
    def rejeitar_usuarios(self, request, queryset):
        """Rejeitar usuários selecionados"""
        rejeitados = 0
        emails_enviados = 0
        
        for usuario in queryset:
            if (usuario.is_profissional or usuario.is_oficina) and usuario.aprovado_pendente:
                # Enviar email de rejeição
                motivo = "Dados fornecidos não atendem aos critérios de aprovação da plataforma"
                
                try:
                    if enviar_email_rejeicao(usuario, motivo):
                        emails_enviados += 1
                        try:
                            self.message_user(request, f'✅ Email de rejeição enviado para {usuario.username} ({usuario.email})', level=messages.SUCCESS)
                        except:
                            pass  # Ignorar erros de mensagens
                    else:
                        try:
                            self.message_user(request, f'⚠️ Falha no envio do email de rejeição para {usuario.username}', level=messages.WARNING)
                        except:
                            pass  # Ignorar erros de mensagens
                except Exception as e:
                    try:
                        self.message_user(request, f'❌ Erro ao enviar email para {usuario.username}: {str(e)}', level=messages.ERROR)
                    except:
                        pass  # Ignorar erros de mensagens
                
                # Desativar usuário rejeitado
                usuario.is_active = False
                usuario.aprovado_pendente = False  # Remove da lista de pendentes
                usuario.save()
                rejeitados += 1
                
            else:
                # Explicar por que não foi rejeitado
                motivos = []
                if not (usuario.is_profissional or usuario.is_oficina):
                    motivos.append("não é profissional/oficina")
                if not usuario.aprovado_pendente:
                    motivos.append("não está pendente")
                
                try:
                    self.message_user(request, f'⏭️ {usuario.username} não foi rejeitado: {", ".join(motivos)}', level=messages.INFO)
                except:
                    pass  # Ignorar erros de mensagens
        
        # Resumo final
        if rejeitados > 0:
            try:
                self.message_user(request, f'🚫 REJEIÇÃO CONCLUÍDA: {rejeitados} usuário(s) rejeitado(s), {emails_enviados} email(s) enviado(s)', level=messages.SUCCESS)
            except:
                pass  # Ignorar erros de mensagens
        else:
            try:
                self.message_user(request, '⚠️ Nenhum usuário foi rejeitado. Verifique os critérios de seleção.', level=messages.WARNING)
            except:
                pass  # Ignorar erros de mensagens
    
    rejeitar_usuarios.short_description = "Rejeitar usuários selecionados"

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
    ordering = ('ordem',)
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
    search_fields = ('item_checklist__checklist__nome', 'observacoes')
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
