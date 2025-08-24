from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
import random
import string

# Create your models here.

class Usuario(AbstractUser):
    is_profissional = models.BooleanField(default=False)
    is_oficina = models.BooleanField(default=False)
    telefone = models.CharField(max_length=20, blank=True)
    email_verificado = models.BooleanField(default=False)
    aprovado_pendente = models.BooleanField(default=False, help_text="Aguardando aprovação do administrador")
    is_admin_oficina = models.BooleanField(default=False)
    # Outros campos relevantes
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        db_table = 'usuarios'

class CodigoVerificacao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=6)
    data_criacao = models.DateTimeField(auto_now_add=True)
    usado = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Código para {self.usuario.email}: {self.codigo}"
    
    def gerar_codigo(self):
        """Gera um código de 6 dígitos"""
        return ''.join(random.choices(string.digits, k=6))
    
    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = self.gerar_codigo()
        super().save(*args, **kwargs)
    
    def expirado(self):
        """Verifica se o código expirou (24 horas)"""
        return timezone.now() > self.data_criacao + timedelta(hours=24)
    
    def valido(self):
        """Verifica se o código é válido e não foi usado"""
        return not self.usado and not self.expirado()
    
    class Meta:
        verbose_name = 'Código de Verificação'
        verbose_name_plural = 'Códigos de Verificação'
        db_table = 'codigo_verificacao'
        ordering = ['-data_criacao']
        
class Veiculo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='veiculos')
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    ano = models.IntegerField()
    placa = models.CharField(max_length=10)
    km_atual = models.PositiveIntegerField(default=0)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='veiculos_criado')
    updated_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='veiculos_atualizado')

    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.placa}"
    
    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        db_table = 'veiculos'
        ordering = ['marca', 'modelo', 'placa']
        
class Oficina(models.Model):
    nome = models.CharField(max_length=200)
    endereco = models.TextField()
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    site = models.URLField(blank=True)
    cnpj = models.CharField(max_length=18)
    aprovado = models.BooleanField(default=False)
    numero_usuarios = models.IntegerField(default=2)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='oficinas_criado')
    updated_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='oficinas_atualizado')
    
    class Meta:
        verbose_name = 'Oficina'
        verbose_name_plural = 'Oficinas'
        db_table = 'oficinas'
        ordering = ['nome']
     
class Profissional(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_profissional')
    especialidade = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    aprovado = models.BooleanField(default=False)
    oficina = models.ForeignKey(Oficina, on_delete=models.CASCADE, related_name='profissionais', null=True, blank=True)
    cnpj = models.CharField(max_length=18, blank=True, help_text="CNPJ da oficina")
    endereco = models.TextField(blank=True, help_text="Endereço da oficina")
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='profissionais_criado')
    updated_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='profissionais_atualizado')

    def __str__(self):
        return f"{self.oficina.nome if self.oficina else self.usuario.username} - {self.especialidade}"
    
    class Meta:
        verbose_name = 'Profissional'
        verbose_name_plural = 'Profissionais'
        db_table = 'profissionais'
        ordering = ['oficina', 'especialidade']
    # Outros campos relevantes

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco_sugerido = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='servicos_criado')
    updated_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='servicos_atualizado')

    def __str__(self):
        return f"{self.nome} - {self.preco_sugerido}"
    
    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
        db_table = 'servicos'
        ordering = ['nome']
    # Outros campos relevantes

class Manutencao(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='manutencoes')
    servico = models.ForeignKey(Servico, on_delete=models.SET_NULL, null=True)
    profissional = models.ForeignKey(Profissional, on_delete=models.SET_NULL, null=True, blank=True)
    data = models.DateField()
    km = models.PositiveIntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    observacoes = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='manutencoes_criado')
    updated_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='manutencoes_atualizado')
    # Outros campos relevantes
    
    class Meta:
        verbose_name = 'Manutenção'
        verbose_name_plural = 'Manutenções'
        db_table = 'manutencoes'
        ordering = ['veiculo__placa', 'data']

    def __str__(self):
        return f"{self.veiculo.placa} - {self.data} - {self.valor}"

class Avaliacao(models.Model):
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE, related_name='avaliacoes')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nota = models.PositiveSmallIntegerField()
    comentario = models.TextField(blank=True)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        db_table = 'avaliacoes'
        ordering = ['profissional__oficina', 'usuario__username', '-data']

    def __str__(self):
        return f"Avaliação de {self.profissional} por {self.usuario} - {self.nota}/5"

class TipoVeiculo(models.Model):
    """Tipos de veículos (carro, moto, caminhão, etc.)"""
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tipos_veiculos')
    data_atualizacao = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='created_by_tipos_veiculos')
    updated_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='updated_by_tipos_veiculos')
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Tipo de Veículo'
        verbose_name_plural = 'Tipos de Veículos'
        db_table = 'tipos_veiculos'
        ordering = ['nome']

class CategoriaChecklist(models.Model):
    """Categorias do checklist (motor, freios, elétrica, etc.)"""
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    ordem = models.PositiveIntegerField(default=0, help_text="Ordem de exibição")
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='categorias_checklist')
    data_atualizacao = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='categorias_checklist_criado')
    updated_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='categorias_checklist_atualizado')
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Categoria do Checklist'
        verbose_name_plural = 'Categorias do Checklist'
        db_table = 'categorias_checklist'
        ordering = ['ordem', 'nome']

class ItemChecklist(models.Model):
    """Itens individuais do checklist"""
    categoria = models.ForeignKey(CategoriaChecklist, on_delete=models.CASCADE, related_name='itens')
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    tipo_verificacao = models.CharField(
        max_length=20,
        choices=[
            ('visual', 'Verificação Visual'),
            ('teste', 'Teste Funcional'),
            ('medicao', 'Medição'),
            ('inspecao', 'Inspeção Detalhada'),
        ],
        default='visual'
    )
    critico = models.BooleanField(default=False, help_text="Item crítico para segurança")
    ordem = models.PositiveIntegerField(default=0, help_text="Ordem dentro da categoria")
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    tipo_resultado = models.CharField(choices=[('1', 'Status'), ('2', 'Valor')], default='1', max_length=10)
    tipo_dado = models.CharField(max_length=10, choices=[('1', 'Numero'), ('2', 'Texto')], default='1')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='itens_checklist')
    obrigatorio = models.BooleanField(default=True, help_text="Item obrigatório no checklist")
    data_atualizacao = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='itens_checklist_criado')
    updated_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='itens_checklist_atualizado')

    def __str__(self):
        return f"{self.categoria.nome} - {self.nome}"
    
    class Meta:
        verbose_name = 'Item do Checklist'
        verbose_name_plural = 'Itens do Checklist'
        db_table = 'itens_checklist'
        ordering = ['ordem', 'nome']

class Checklist(models.Model):
    """Checklist personalizado de uma oficina para um tipo de veículo"""
    oficina = models.ForeignKey(Oficina, on_delete=models.CASCADE, related_name='checklists')
    tipo_veiculo = models.ForeignKey(TipoVeiculo, on_delete=models.CASCADE, related_name='checklists')
    nome = models.CharField(max_length=200, help_text="Nome do checklist (ex: Checklist Preventiva Carros)")
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='checklists')
    updated_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='checklists_atualizados')
    
    def __str__(self):
        return f"{self.oficina.nome} - {self.tipo_veiculo.nome} - {self.nome}"
    
    class Meta:
        verbose_name = 'Checklist'
        verbose_name_plural = 'Checklists'
        db_table = 'checklists'
        ordering = ['oficina__nome', 'tipo_veiculo__nome', 'nome']
        unique_together = ['oficina', 'tipo_veiculo']

class ItemChecklistPersonalizado(models.Model):
    """Itens personalizados do checklist da oficina"""
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name='itens_personalizados')
    item_padrao = models.ForeignKey(ItemChecklist, on_delete=models.CASCADE, null=True, blank=True, 
                                   help_text="Item padrão do sistema (opcional)")

    critico = models.BooleanField(default=False)
    obrigatorio = models.BooleanField(default=True, help_text="Item obrigatório no checklist")
    ordem = models.PositiveIntegerField(default=0)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='itens_checklist_personalizados_criado')
    updated_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='itens_checklist_personalizados_atualizado')
    
    def __str__(self):
        return f"{self.checklist.nome} - Item {self.ordem}"
    
    class Meta:
        verbose_name = 'Item Personalizado do Checklist'
        verbose_name_plural = 'Itens Personalizados do Checklist'
        db_table = 'itens_checklist_personalizados'
        ordering = ['checklist', 'ordem']

class ChecklistExecutado(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name='checklist_executado')
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='checklists_executados', 
                               help_text="Veículo que está sendo verificado", null=True, blank=True)
    data_execucao = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='checklist_executado')
    observacoes = models.TextField(blank=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, choices=[('pendente', 'Pendente'), ('executado', 'Executado'), ('cancelado', 'Cancelado')], default='pendente')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='checklist_executado_criado')
    updated_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='checklist_executado_atualizado')

    class Meta:
        verbose_name = 'Checklist Executado'
        verbose_name_plural = 'Checklists Executados'
        db_table = 'checklist_executado'
        ordering = ['checklist', 'data_execucao']

    def __str__(self):
        veiculo_info = f" - {self.veiculo.placa}" if self.veiculo else ""
        return f"{self.checklist.oficina.nome}{veiculo_info} - {self.data_execucao}"
    
    def get_progresso(self):
        """Calcula o progresso do checklist executado"""
        total_itens = self.itens_executados.count()
        if total_itens == 0:
            return {'percentual': 0, 'concluidos': 0, 'total': 0}
        
        # Contar itens que não estão pendentes (resultado != '4')
        itens_concluidos = self.itens_executados.exclude(resultado='4').count()
        percentual = round((itens_concluidos / total_itens) * 100)
        
        return {
            'percentual': percentual,
            'concluidos': itens_concluidos,
            'total': total_itens
        }
    
    def get_progresso_display(self):
        """Retorna uma string formatada do progresso"""
        progresso = self.get_progresso()
        return f"{progresso['concluidos']}/{progresso['total']} ({progresso['percentual']}%)"
    
class ItemChecklistExecutado(models.Model):
    checklist_executado = models.ForeignKey(ChecklistExecutado, on_delete=models.CASCADE, related_name='itens_executados')
    item_checklist = models.ForeignKey(ItemChecklistPersonalizado, on_delete=models.CASCADE, related_name='itens_checklist_executados')
    resultado = models.CharField(choices=[('1', 'OK'), ('2', 'Atenção'), ('3', 'Problema'),('4', 'Pendente')],  default='4', max_length=10)
    valor_resultado = models.CharField(max_length=30, blank=True, null=True)
    observacoes = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='itens_checklist_executado_criado')
    updated_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='itens_checklist_executado_atualizado')
    
    class Meta:
        verbose_name = 'Item Checklist Executado'
        verbose_name_plural = 'Itens Checklist Executados'
        db_table = 'itens_checklist_executado'
        ordering = ['checklist_executado', 'item_checklist__ordem', 'resultado']
            
class Arquivos_checklist(models.Model):
    item_checklist_executado = models.ForeignKey(ItemChecklistExecutado, on_delete=models.CASCADE, related_name='arquivos')
    arquivo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=30, choices=[('foto', 'Foto'), ('documento', 'Documento')])
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='arquivos_checklist_criado')
    updated_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='arquivos_checklist_atualizado')
    
    class Meta:
        verbose_name = 'Arquivo Checklist'
        verbose_name_plural = 'Arquivos Checklist'
        db_table = 'arquivos_checklist'
        ordering = ['item_checklist_executado', 'arquivo']

    def __str__(self):
        return f"{self.item_checklist_executado.checklist_executado.checklist.oficina.nome} - {self.item_checklist_executado.checklist_executado.checklist.tipo_veiculo.nome} - {self.arquivo}"
      
class UsuarioOficina(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuario_oficina')
    oficina = models.ForeignKey(Oficina, on_delete=models.CASCADE, related_name='usuario_oficina')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)
    created_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuario_oficina_criado')
    updated_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuario_oficina_atualizado')
    
    class Meta:
        verbose_name = 'Usuário Oficina'
        verbose_name_plural = 'Usuários Oficinas'
        db_table = 'usuario_oficina'
        ordering = ['usuario', 'oficina']


    def __str__(self):
        return f"{self.usuario.username} - {self.oficina.nome}"