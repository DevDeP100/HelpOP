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

    def __str__(self):
        return f"{self.nome_oficina} - {self.especialidade}"
    
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
        return f"{self.profissional.nome_oficina} - {self.usuario.username} - {self.nota}"

