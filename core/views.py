from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Sum, Count, Q, Avg, Max
from django.utils import timezone
from datetime import datetime, timedelta
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from io import BytesIO
from .models import (
    Usuario, Veiculo, Manutencao, Profissional, Servico,
    TipoVeiculo, CategoriaChecklist, ItemChecklist, Checklist, 
    ItemChecklistPersonalizado, ChecklistExecutado, ItemChecklistExecutado, Arquivos_checklist, UsuarioOficina
)
from .forms import UsuarioForm, VeiculoForm, ManutencaoForm
from .email_utils import enviar_codigo_verificacao, verificar_codigo
from .decorators import profissional_required, oficina_required

def home(request):
    """Página inicial do sistema"""
    return render(request, 'home.html')

def login_view(request):
    """View para login de usuários"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Administradores não precisam de verificação de email
            if not user.is_staff and not user.email_verificado:
                messages.error(request, 'Por favor, verifique seu email antes de fazer login.')
                return redirect('verificar_email', user_id=user.id)
            
            # Verificar se profissional/oficina está aprovado (exceto administradores)
            if not user.is_staff and (user.is_profissional or user.is_oficina) and user.aprovado_pendente:
                # Não fazer login, apenas mostrar mensagem na tela
                context = {
                    'pending_approval': True,
                    'user_type': 'Profissional' if user.is_profissional else 'Oficina',
                    'username': username
                }
                return render(request, 'auth/login.html', context)
            
            login(request, user)
            messages.success(request, f'Bem-vindo de volta, {user.get_full_name() or user.username}!')
            return redirect('checklist_gerenciar')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
    
    return render(request, 'auth/login.html')

def cadastro_view(request):
    """View para cadastro de novos usuários"""
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            
            # Se for profissional ou oficina, marcar como pendente de aprovação
            if form.cleaned_data.get('is_profissional') or form.cleaned_data.get('is_oficina'):
                user.aprovado_pendente = True
            
            user.save()
            
            # Se for profissional ou oficina, criar perfil profissional
            if form.cleaned_data.get('is_profissional') or form.cleaned_data.get('is_oficina'):
                Profissional.objects.create(
                    usuario=user,
                    created_by=user,
                    updated_by=user
                )
            
            # Para administradores, não enviar código de verificação
            if user.is_staff:
                user.email_verificado = True
                user.save()
                messages.success(request, 'Conta de administrador criada com sucesso!')
                return redirect('login')
            
            # Enviar código de verificação para usuários normais
            if enviar_codigo_verificacao(user):
                messages.success(request, 'Conta criada com sucesso! Verifique seu email para confirmar o cadastro.')
                return redirect('verificar_email', user_id=user.id)
            else:
                messages.error(request, 'Erro ao enviar código de verificação. Tente novamente.')
                user.delete()  # Deletar usuário se falhar no envio
                return redirect('cadastro')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UsuarioForm()
    
    return render(request, 'auth/cadastro.html', {'form': form})

def verificar_email(request, user_id):
    """View para verificação de email"""
    user = get_object_or_404(Usuario, id=user_id)
    
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        
        if verificar_codigo(user, codigo):
            if user.is_profissional or user.is_oficina:
                messages.success(request, 'Email verificado com sucesso! Sua conta está aguardando aprovação do administrador. Você receberá uma notificação quando for aprovado.')
            else:
                messages.success(request, 'Email verificado com sucesso! Faça login para continuar.')
            return redirect('login')
        else:
            messages.error(request, 'Código inválido ou expirado. Tente novamente.')
    
    return render(request, 'auth/verificar_email.html', {'user': user})

def reenviar_codigo(request, user_id):
    """View para reenviar código de verificação"""
    user = get_object_or_404(Usuario, id=user_id)
    
    if enviar_codigo_verificacao(user):
        messages.success(request, 'Código reenviado com sucesso! Verifique seu email.')
    else:
        messages.error(request, 'Erro ao reenviar código. Tente novamente.')
    
    return redirect('verificar_email', user_id=user.id)

def logout_view(request):
    """View para logout de usuários"""
    logout(request)
    messages.success(request, 'Você saiu do sistema com sucesso.')
    return redirect('home')

@login_required
def dashboard(request):
    """Dashboard principal do usuário"""
    # Estatísticas do usuário
    veiculos_count = Veiculo.objects.filter(usuario=request.user).count()
    manutencoes_count = Manutencao.objects.filter(veiculo__usuario=request.user).count()
    
    # Total gasto em manutenções
    total_gasto = Manutencao.objects.filter(
        veiculo__usuario=request.user
    ).aggregate(total=Sum('valor'))['total'] or 0
    
    # Próximas manutenções (exemplo simples)
    proximas_manutencoes = 0  # Implementar lógica de alertas
    
    # Veículos do usuário
    veiculos = Veiculo.objects.filter(usuario=request.user)
    
    # Manutenções recentes
    manutencoes_recentes = Manutencao.objects.filter(
        veiculo__usuario=request.user
    ).order_by('-data')[:5]
    
    context = {
        'veiculos_count': veiculos_count,
        'manutencoes_count': manutencoes_count,
        'total_gasto': f"{total_gasto:.2f}",
        'proximas_manutencoes': proximas_manutencoes,
        'veiculos': veiculos,
        'manutencoes_recentes': manutencoes_recentes,
    }
    
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def perfil(request):
    """Página de perfil do usuário"""
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')
    else:
        form = UsuarioForm(instance=request.user)
    
    return render(request, 'perfil/perfil.html', {'form': form})

@login_required
def veiculos(request):
    """Lista de veículos - Diferente para usuários e profissionais"""
    if request.user.is_profissional or request.user.is_oficina:
        # Profissionais veem todos os veículos
        veiculos = Veiculo.objects.all()
    else:
        # Usuários comuns veem apenas seus veículos
        veiculos = Veiculo.objects.filter(usuario=request.user)
    
    return render(request, 'veiculos/lista.html', {'veiculos': veiculos})

@login_required
def adicionar_veiculo(request):
    """Adicionar novo veículo"""
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            veiculo = form.save(commit=False)
            veiculo.usuario = request.user
            veiculo.save()
            messages.success(request, 'Veículo adicionado com sucesso!')
            return redirect('veiculos')
    else:
        form = VeiculoForm()
    
    return render(request, 'veiculos/form.html', {'form': form, 'titulo': 'Adicionar Veículo'})

@login_required
def editar_veiculo(request, veiculo_id):
    """Editar veículo existente"""
    veiculo = get_object_or_404(Veiculo, id=veiculo_id, usuario=request.user)
    
    if request.method == 'POST':
        form = VeiculoForm(request.POST, instance=veiculo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Veículo atualizado com sucesso!')
            return redirect('veiculos')
    else:
        form = VeiculoForm(instance=veiculo)
    
    return render(request, 'veiculos/form.html', {'form': form, 'titulo': 'Editar Veículo'})

@login_required
def veiculo_detalhes(request, veiculo_id):
    """Detalhes do veículo"""
    veiculo = get_object_or_404(Veiculo, id=veiculo_id, usuario=request.user)
    manutencoes = Manutencao.objects.filter(veiculo=veiculo).order_by('-data')
    
    return render(request, 'veiculos/detalhes.html', {
        'veiculo': veiculo,
        'manutencoes': manutencoes
    })

@login_required
def manutencoes(request):
    """Lista de manutenções - Diferente para usuários e profissionais"""
    if request.user.is_profissional or request.user.is_oficina:
        # Profissionais veem todas as manutenções que eles fizeram
        manutencoes = Manutencao.objects.filter(profissional__usuario=request.user).order_by('-data')
    else:
        # Usuários comuns veem apenas suas manutenções
        manutencoes = Manutencao.objects.filter(veiculo__usuario=request.user).order_by('-data')
    
    return render(request, 'manutencoes/lista.html', {'manutencoes': manutencoes})

@login_required
@profissional_required
def nova_manutencao(request, veiculo_id=None):
    """Adicionar nova manutenção - Apenas profissionais e oficinas"""
    if request.method == 'POST':
        form = ManutencaoForm(request.POST, user=request.user)
        if form.is_valid():
            manutencao = form.save(commit=False)
            if veiculo_id:
                manutencao.veiculo_id = veiculo_id
            else:
                manutencao.veiculo = form.cleaned_data['veiculo']
            manutencao.save()
            messages.success(request, 'Manutenção registrada com sucesso!')
            return redirect('manutencoes')
    else:
        initial = {}
        if veiculo_id:
            initial['veiculo'] = veiculo_id
        form = ManutencaoForm(initial=initial, user=request.user)
    
    return render(request, 'manutencoes/form.html', {'form': form, 'titulo': 'Nova Manutenção'})

def servicos(request):
    """Lista de serviços disponíveis"""
    servicos = Servico.objects.all()
    return render(request, 'servicos/lista.html', {'servicos': servicos})

def profissionais(request):
    """Lista de profissionais"""
    profissionais = Profissional.objects.filter(aprovado=True)
    return render(request, 'profissionais/lista.html', {'profissionais': profissionais})

@login_required
def buscar_profissionais(request):
    """Buscar profissionais por localização/serviço"""
    profissionais = Profissional.objects.filter(aprovado=True)
    return render(request, 'profissionais/busca.html', {'profissionais': profissionais})

# Views para administração de aprovações
@login_required
def admin_aprovar_usuarios(request):
    """View para administrador aprovar usuários pendentes"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores podem acessar esta página.')
        return redirect('home')
    
    # Buscar usuários pendentes de aprovação
    usuarios_pendentes = Usuario.objects.filter(
        aprovado_pendente=True,
        email_verificado=True
    ).order_by('date_joined')
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')  # 'aprovar' ou 'rejeitar'
        
        try:
            user = Usuario.objects.get(id=user_id, aprovado_pendente=True)
            
            if action == 'aprovar':
                user.aprovado_pendente = False
                user.save()
                
                # Se for profissional, aprovar o perfil também
                if hasattr(user, 'perfil_profissional'):
                    user.perfil_profissional.aprovado = True
                    user.perfil_profissional.save()
                
                # Enviar email de aprovação
                try:
                    from .email_utils import enviar_email_aprovacao
                    if enviar_email_aprovacao(user):
                        messages.success(request, f'Usuário {user.get_full_name()} aprovado e email enviado com sucesso!')
                    else:
                        messages.warning(request, f'Usuário {user.get_full_name()} aprovado, mas falha no envio do email.')
                except Exception as e:
                    messages.success(request, f'Usuário {user.get_full_name()} aprovado com sucesso!')
                    messages.warning(request, f'Email não foi enviado devido a um erro técnico.')
                
            elif action == 'rejeitar':
                # Enviar email de rejeição antes de deletar
                try:
                    from .email_utils import enviar_email_rejeicao
                    motivo = "Dados fornecidos não atendem aos critérios de aprovação da plataforma"
                    if enviar_email_rejeicao(user, motivo):
                        messages.success(request, f'Email de rejeição enviado e usuário removido do sistema.')
                    else:
                        messages.warning(request, f'Usuário rejeitado, mas falha no envio do email.')
                except Exception as e:
                    messages.success(request, f'Usuário rejeitado e removido do sistema.')
                    messages.warning(request, f'Email não foi enviado devido a um erro técnico.')
                
                # Deletar o usuário rejeitado
                user.delete()
                
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')
    
    return render(request, 'admin/aprovar_usuarios.html', {
        'usuarios_pendentes': usuarios_pendentes
    })

@login_required
def admin_usuario_detalhes(request, user_id):
    """View para mostrar detalhes de um usuário pendente de aprovação"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores podem acessar esta página.')
        return redirect('home')
    usuario = get_object_or_404(Usuario, id=user_id)
    return render(request, 'admin/usuario_detalhes.html', {'usuario': usuario})

@login_required
def admin_dashboard(request):
    """Dashboard do administrador"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores podem acessar esta página.')
        return redirect('home')
    
    # Estatísticas para o administrador
    total_usuarios = Usuario.objects.count()
    usuarios_pendentes = Usuario.objects.filter(aprovado_pendente=True).count()
    
    # Profissionais aprovados (apenas profissionais, não oficinas)
    profissionais_aprovados = Usuario.objects.filter(
        is_profissional=True, 
        is_oficina=False,  # Não é oficina
        aprovado_pendente=False,
        is_active=True
    ).count()
    
    # Oficinas aprovadas (apenas oficinas, não profissionais simples)
    oficinas_aprovadas = Usuario.objects.filter(
        is_oficina=True, 
        aprovado_pendente=False,
        is_active=True
    ).count()
    
    # Usuários pendentes recentes
    usuarios_pendentes_recentes = Usuario.objects.filter(
        aprovado_pendente=True,
        email_verificado=True
    ).order_by('-date_joined')[:5]
    
    context = {
        'total_usuarios': total_usuarios,
        'usuarios_pendentes': usuarios_pendentes,
        'profissionais_aprovados': profissionais_aprovados,
        'oficinas_aprovadas': oficinas_aprovadas,
        'usuarios_pendentes_recentes': usuarios_pendentes_recentes,
    }
    
    return render(request, 'admin/dashboard.html', context)

@login_required
def admin_gerenciar_usuarios(request):
    """View para gerenciar todos os usuários do sistema"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores podem acessar esta página.')
        return redirect('home')
    
    # Filtros
    tipo_filtro = request.GET.get('tipo', '')
    status_filtro = request.GET.get('status', '')
    busca = request.GET.get('busca', '')
    
    # Query base
    usuarios = Usuario.objects.all()
    
    # Aplicar filtros
    if tipo_filtro:
        if tipo_filtro == 'profissional':
            usuarios = usuarios.filter(is_profissional=True)
        elif tipo_filtro == 'oficina':
            usuarios = usuarios.filter(is_oficina=True)
        elif tipo_filtro == 'usuario':
            usuarios = usuarios.filter(is_profissional=False, is_oficina=False)
    
    if status_filtro:
        if status_filtro == 'pendente':
            usuarios = usuarios.filter(aprovado_pendente=True)
        elif status_filtro == 'aprovado':
            usuarios = usuarios.filter(aprovado_pendente=False)
        elif status_filtro == 'email_nao_verificado':
            usuarios = usuarios.filter(email_verificado=False)
    
    if busca:
        usuarios = usuarios.filter(
            Q(username__icontains=busca) |
            Q(first_name__icontains=busca) |
            Q(last_name__icontains=busca) |
            Q(email__icontains=busca)
        )
    
    # Ordenação
    usuarios = usuarios.order_by('-date_joined')
    
    # Ações
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        
        try:
            user = Usuario.objects.get(id=user_id)
            
            if action == 'aprovar':
                user.aprovado_pendente = False
                user.save()
                if hasattr(user, 'perfil_profissional'):
                    user.perfil_profissional.aprovado = True
                    user.perfil_profissional.save()
                messages.success(request, f'Usuário {user.username} aprovado com sucesso!')
                
            elif action == 'rejeitar':
                user.delete()
                messages.success(request, f'Usuário removido do sistema.')
                
            elif action == 'ativar':
                user.is_active = True
                user.save()
                messages.success(request, f'Usuário {user.username} ativado.')
                
            elif action == 'desativar':
                user.is_active = False
                user.save()
                messages.success(request, f'Usuário {user.username} desativado.')
                
            elif action == 'tornar_staff':
                user.is_staff = True
                user.save()
                messages.success(request, f'Usuário {user.username} agora é administrador.')
                
            elif action == 'remover_staff':
                user.is_staff = False
                user.save()
                messages.success(request, f'Usuário {user.username} não é mais administrador.')
                
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')
    
    context = {
        'usuarios': usuarios,
        'tipo_filtro': tipo_filtro,
        'status_filtro': status_filtro,
        'busca': busca,
    }
    
    return render(request, 'admin/gerenciar_usuarios.html', context)

@login_required
@profissional_required
def profissional_dashboard(request):
    """Dashboard específico para profissionais e oficinas"""
    # Manutenções realizadas pelo profissional
    manutencoes_realizadas = Manutencao.objects.filter(
        profissional__usuario=request.user
    ).order_by('-data')
    
    # Estatísticas
    total_manutencoes = manutencoes_realizadas.count()
    total_valor = manutencoes_realizadas.aggregate(total=Sum('valor'))['total'] or 0
    
    # Manutenções por mês (últimos 6 meses)
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    hoje = timezone.now().date()
    meses_atras = []
    for i in range(6):
        data = hoje - timedelta(days=30*i)
        mes_manutencoes = manutencoes_realizadas.filter(
            data__year=data.year,
            data__month=data.month
        ).count()
        meses_atras.append({
            'mes': data.strftime('%b/%Y'),
            'quantidade': mes_manutencoes
        })
    
    # Veículos disponíveis para manutenção
    veiculos_disponiveis = Veiculo.objects.all().order_by('usuario__first_name', 'marca', 'modelo')
    
    context = {
        'manutencoes_realizadas': manutencoes_realizadas[:10],  # Últimas 10
        'total_manutencoes': total_manutencoes,
        'total_valor': total_valor,
        'meses_atras': meses_atras,
        'veiculos_disponiveis': veiculos_disponiveis,
    }
    
    return render(request, 'profissional/dashboard.html', context)

@login_required
@profissional_required
def profissional_manutencoes(request):
    """Lista de todas as manutenções realizadas pelo profissional"""
    manutencoes = Manutencao.objects.filter(
        profissional__usuario=request.user
    ).order_by('-data')
    
    # Filtros
    veiculo_filtro = request.GET.get('veiculo', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    if veiculo_filtro:
        manutencoes = manutencoes.filter(veiculo__placa__icontains=veiculo_filtro)
    
    if data_inicio:
        manutencoes = manutencoes.filter(data__gte=data_inicio)
    
    if data_fim:
        manutencoes = manutencoes.filter(data__lte=data_fim)
    
    context = {
        'manutencoes': manutencoes,
        'veiculo_filtro': veiculo_filtro,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    
    return render(request, 'profissional/manutencoes.html', context)

@login_required
@profissional_required
def profissional_nova_manutencao(request):
    """Criar nova manutenção para qualquer veículo"""
    if request.method == 'POST':
        form = ManutencaoForm(request.POST, user=request.user)
        if form.is_valid():
            manutencao = form.save(commit=False)
            # Associar o profissional atual
            if hasattr(request.user, 'perfil_profissional'):
                manutencao.profissional = request.user.perfil_profissional
            manutencao.save()
            messages.success(request, 'Manutenção registrada com sucesso!')
            return redirect('profissional_manutencoes')
    else:
        form = ManutencaoForm(user=request.user)
    
    # Buscar veículos por placa
    placa_busca = request.GET.get('placa', '')
    veiculos = Veiculo.objects.all()
    if placa_busca:
        veiculos = veiculos.filter(placa__icontains=placa_busca)
    
    context = {
        'form': form,
        'veiculos': veiculos,
        'placa_busca': placa_busca,
    }
    
    return render(request, 'profissional/nova_manutencao.html', context)

@login_required
@profissional_required
def profissional_editar_manutencao(request, manutencao_id):
    """Editar manutenção existente"""
    manutencao = get_object_or_404(Manutencao, id=manutencao_id, profissional__usuario=request.user)
    
    if request.method == 'POST':
        form = ManutencaoForm(request.POST, instance=manutencao, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Manutenção atualizada com sucesso!')
            return redirect('profissional_manutencoes')
    else:
        form = ManutencaoForm(instance=manutencao, user=request.user)
    
    return render(request, 'profissional/editar_manutencao.html', {
        'form': form,
        'manutencao': manutencao
    })

# Views para o sistema de Checklist
@login_required
def checklist_lista(request):
    """Lista todos os checklists disponíveis"""
   
    if request.user.is_oficina:
        # Oficinas veem seus próprios checklists
        try:
            oficina = UsuarioOficina.objects.get(usuario=request.user)
            if oficina:
                checklists = Checklist.objects.filter(oficina=oficina.oficina)
            else:
                checklists = Checklist.objects.none()
        except Exception as e:
            print(50*'=')
            print('Erro: ', e)
            print(50*'=')
            checklists = Checklist.objects.none()
    elif request.user.is_profissional:
        # Profissionais veem checklists das oficinas onde trabalham
        profissional = get_object_or_404(Profissional, usuario=request.user)
        checklists = Checklist.objects.filter(oficina=profissional.oficina)
    else:
        # Usuários normais veem todos os checklists ativos
        checklists = Checklist.objects.filter(ativo=True)
    
    context = {
        'checklists': checklists,
        'tipos_veiculos': TipoVeiculo.objects.filter(ativo=True),
    }
    return render(request, 'checklist/lista.html', context)

@login_required
@oficina_required
def checklist_criar(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao', '')
        tipo_veiculo_id = request.POST.get('tipo_veiculo')
        
        if nome and tipo_veiculo_id:
            tipo_veiculo = get_object_or_404(TipoVeiculo, id=tipo_veiculo_id)
            
            # Pegar a oficina através da tabela UsuarioOficina
            try:
                oficina_rel = UsuarioOficina.objects.get(usuario=request.user)
                oficina = oficina_rel.oficina
                
                if not oficina:
                    messages.error(request, 'Você não possui uma oficina associada. Entre em contato com o administrador.')
                    return redirect('checklist_lista')
                    
                # Verificar se já existe um checklist para esta oficina e tipo de veículo
                checklist_existente = Checklist.objects.filter(
                    oficina=oficina,
                    tipo_veiculo=tipo_veiculo
                ).first()
                
                if checklist_existente:
                    messages.error(
                        request, 
                        f'Já existe um checklist para o tipo de veículo "{tipo_veiculo.nome}" '
                        f'nesta oficina: "{checklist_existente.nome}". '
                        f'Cada oficina pode ter apenas um checklist por tipo de veículo.'
                    )
                    context = {
                        'tipos_veiculos': TipoVeiculo.objects.filter(ativo=True),
                        'categorias': CategoriaChecklist.objects.filter(ativo=True).order_by('ordem'),
                        'form_data': {
                            'nome': nome,
                            'descricao': descricao,
                            'tipo_veiculo': tipo_veiculo_id
                        }
                    }
                    return render(request, 'checklist/criar.html', context)
                
            except UsuarioOficina.DoesNotExist:
                messages.error(request, 'Você não possui uma oficina associada. Entre em contato com o administrador.')
                return redirect('checklist_lista')
            
            # Se chegou até aqui, pode criar o checklist
            checklist = Checklist.objects.create(
                oficina=oficina,
                tipo_veiculo=tipo_veiculo,
                nome=nome,
                descricao=descricao,
                created_by=request.user,
                updated_by=request.user
            )
            
            messages.success(request, f'Checklist "{nome}" criado com sucesso!')
            return redirect('checklist_detalhes', checklist_id=checklist.id)
        else:
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
    
    context = {
        'tipos_veiculos': TipoVeiculo.objects.filter(ativo=True),
        'categorias': CategoriaChecklist.objects.filter(ativo=True).order_by('ordem'),
    }
    return render(request, 'checklist/criar.html', context)

@login_required
def checklist_detalhes(request, checklist_id):
    """Detalhes de um checklist específico"""
    checklist = get_object_or_404(Checklist, id=checklist_id)
    
    # Verificar permissões
    if not request.user.is_staff:
        if request.user.is_oficina:
            try:
                oficina = UsuarioOficina.objects.get(usuario=request.user)
                if not oficina or checklist.oficina != oficina.oficina:
                    messages.error(request, 'Você não tem permissão para acessar este checklist.')
                    return redirect('checklist_lista')
            except:
                messages.error(request, 'Você não possui uma oficina associada.')
                return redirect('checklist_lista')
        elif request.user.is_profissional:
            profissional = get_object_or_404(Profissional, usuario=request.user)
            if checklist.oficina != profissional.oficina:
                messages.error(request, 'Você não tem permissão para acessar este checklist.')
                return redirect('checklist_lista')
    
    # Filtros para execuções
    execucoes_query = checklist.checklist_executado.all().order_by('-data_execucao')
    
    # Aplicar filtros
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    veiculo_id = request.GET.get('veiculo')
    usuario_id = request.GET.get('usuario')
    status = request.GET.get('status')
    
    if data_inicio:
        try:
            data_inicio_parsed = datetime.strptime(data_inicio, '%Y-%m-%d')
            execucoes_query = execucoes_query.filter(data_execucao__date__gte=data_inicio_parsed.date())
        except ValueError:
            pass
    
    if data_fim:
        try:
            data_fim_parsed = datetime.strptime(data_fim, '%Y-%m-%d')
            execucoes_query = execucoes_query.filter(data_execucao__date__lte=data_fim_parsed.date())
        except ValueError:
            pass
    
    if veiculo_id:
        execucoes_query = execucoes_query.filter(veiculo_id=veiculo_id)
    
    if usuario_id:
        execucoes_query = execucoes_query.filter(usuario_id=usuario_id)
    
    if status:
        execucoes_query = execucoes_query.filter(status=status)
    
    # Paginação
    paginator = Paginator(execucoes_query, 20)  # 20 registros por página
    page_number = request.GET.get('page')
    execucoes = paginator.get_page(page_number)
    
    # Dados para os filtros
    veiculos_execucoes = checklist.checklist_executado.values_list('veiculo', flat=True).distinct()
    veiculos_filtro = Veiculo.objects.filter(id__in=veiculos_execucoes).order_by('marca', 'modelo')
    
    usuarios_execucoes = checklist.checklist_executado.values_list('usuario', flat=True).distinct()
    usuarios_filtro = Usuario.objects.filter(id__in=usuarios_execucoes).order_by('first_name', 'last_name', 'username')
    
    context = {
        'checklist': checklist,
        'itens_personalizados': checklist.itens_personalizados.filter(ativo=True).order_by('ordem'),
        'execucoes': execucoes,
        'veiculos_filtro': veiculos_filtro,
        'usuarios_filtro': usuarios_filtro,
        'filtros': {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'veiculo': veiculo_id,
            'usuario': usuario_id,
            'status': status,
        }
    }
    return render(request, 'checklist/detalhes.html', context)

@login_required
def checklist_gerenciar_execucoes(request, checklist_id):
    """Gerenciar execuções de um checklist específico"""
    checklist = get_object_or_404(Checklist, id=checklist_id)
    
    # Verificar permissões
    if not request.user.is_staff:
        if request.user.is_oficina:
            try:
                oficina = UsuarioOficina.objects.get(usuario=request.user)
                if not oficina or checklist.oficina != oficina.oficina:
                    messages.error(request, 'Você não tem permissão para acessar este checklist.')
                    return redirect('checklist_lista')
            except:
                messages.error(request, 'Você não possui uma oficina associada.')
                return redirect('checklist_lista')
        elif request.user.is_profissional:
            profissional = get_object_or_404(Profissional, usuario=request.user)
            if checklist.oficina != profissional.oficina:
                messages.error(request, 'Você não tem permissão para acessar este checklist.')
                return redirect('checklist_lista')
    
    # Filtros para execuções
    execucoes_query = checklist.checklist_executado.all().order_by('-data_execucao')
    
    # Aplicar filtros
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    veiculo_id = request.GET.get('veiculo')
    usuario_id = request.GET.get('usuario')
    status = request.GET.get('status')
    
    if data_inicio:
        try:
            data_inicio_parsed = datetime.strptime(data_inicio, '%Y-%m-%d')
            execucoes_query = execucoes_query.filter(data_execucao__date__gte=data_inicio_parsed.date())
        except ValueError:
            pass
    
    if data_fim:
        try:
            data_fim_parsed = datetime.strptime(data_fim, '%Y-%m-%d')
            execucoes_query = execucoes_query.filter(data_execucao__date__lte=data_fim_parsed.date())
        except ValueError:
            pass
    
    if veiculo_id:
        execucoes_query = execucoes_query.filter(veiculo_id=veiculo_id)
    
    if usuario_id:
        execucoes_query = execucoes_query.filter(usuario_id=usuario_id)
    
    if status:
        execucoes_query = execucoes_query.filter(status=status)
    
    # Paginação
    paginator = Paginator(execucoes_query, 20)  # 20 registros por página
    page_number = request.GET.get('page')
    execucoes = paginator.get_page(page_number)
    
    # Dados para os filtros
    veiculos_execucoes = checklist.checklist_executado.values_list('veiculo', flat=True).distinct()
    veiculos_filtro = Veiculo.objects.filter(id__in=veiculos_execucoes).order_by('marca', 'modelo')
    
    usuarios_execucoes = checklist.checklist_executado.values_list('usuario', flat=True).distinct()
    usuarios_filtro = Usuario.objects.filter(id__in=usuarios_execucoes).order_by('first_name', 'last_name', 'username')
    
    context = {
        'checklist': checklist,
        'execucoes': execucoes,
        'veiculos_filtro': veiculos_filtro,
        'usuarios_filtro': usuarios_filtro,
        'filtros': {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'veiculo': veiculo_id,
            'usuario': usuario_id,
            'status': status,
        }
    }
    return render(request, 'checklist/gerenciar_execucoes.html', context)

@login_required
@oficina_required
def checklist_editar(request, checklist_id):
    """Editar checklist"""
    checklist = get_object_or_404(Checklist, id=checklist_id)
    
    # Verificar se o usuário tem permissão para editar
    if not request.user.is_staff:
        if request.user.is_oficina:
            try:
                oficina = UsuarioOficina.objects.get(usuario=request.user)
                if not oficina or checklist.oficina != oficina.oficina:
                    messages.error(request, 'Você não tem permissão para editar este checklist.')
                    return redirect('checklist_lista')
            except:
                messages.error(request, 'Você não possui uma oficina associada.')
                return redirect('checklist_lista')
        elif request.user.is_profissional:
            profissional = get_object_or_404(Profissional, usuario=request.user)
            if checklist.oficina != profissional.oficina:
                messages.error(request, 'Você não tem permissão para editar este checklist.')
                return redirect('checklist_lista')
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao', '')
        ativo = request.POST.get('ativo') == 'on'
        
        if nome:
            checklist.nome = nome
            checklist.descricao = descricao
            checklist.ativo = ativo
            checklist.updated_by = request.user
            checklist.save()
            
            messages.success(request, 'Checklist atualizado com sucesso!')
            return redirect('checklist_detalhes', checklist_id=checklist.id)
        else:
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
    
    context = {
        'checklist': checklist,
        'tipos_veiculos': TipoVeiculo.objects.filter(ativo=True),
    }
    return render(request, 'checklist/editar.html', context)

@login_required
def checklist_executar(request, checklist_id):
    """Executar um checklist"""
    checklist = get_object_or_404(Checklist, id=checklist_id, ativo=True)
    
    # Verificar permissões
    if not request.user.is_staff:
        if request.user.is_oficina:
            try:
                oficina = UsuarioOficina.objects.get(usuario=request.user)
                if not oficina or checklist.oficina != oficina.oficina:
                    messages.error(request, 'Você não tem permissão para executar este checklist.')
                    return redirect('checklist_lista')
            except:
                messages.error(request, 'Você não possui uma oficina associada.')
                return redirect('checklist_lista')
        elif request.user.is_profissional:
            profissional = get_object_or_404(Profissional, usuario=request.user)
            if checklist.oficina != profissional.oficina:
                messages.error(request, 'Você não tem permissão para executar este checklist.')
                return redirect('checklist_lista')
    
    if request.method == 'POST':
        # Criar execução do checklist
        observacoes = request.POST.get('observacoes', '')
        veiculo_id = request.POST.get('veiculo')
        
        if not veiculo_id:
            messages.error(request, 'Por favor, selecione um veículo.')
            context = {
                'checklist': checklist,
                'itens_personalizados': checklist.itens_personalizados.filter(ativo=True).order_by('ordem'),
                'veiculos': Veiculo.objects.all().order_by('marca', 'modelo'),
            }
            return render(request, 'checklist/executar.html', context)
        
        veiculo = get_object_or_404(Veiculo, id=veiculo_id)
        
        checklist_executado = ChecklistExecutado.objects.create(
            checklist=checklist,
            veiculo=veiculo,
            usuario=request.user,
            observacoes=observacoes,
            created_by=request.user,
            updated_by=request.user
        )
        
        # Criar itens executados baseados nos itens personalizados
        # Verificar se já existem itens executados para evitar duplicação
        itens_existentes = checklist_executado.itens_executados.values_list('item_checklist_id', flat=True)
        
        for item_personalizado in checklist.itens_personalizados.filter(ativo=True):
            if item_personalizado.id not in itens_existentes:
                ItemChecklistExecutado.objects.create(
                    checklist_executado=checklist_executado,
                    item_checklist=item_personalizado,
                    resultado='4',  # '4' = Pendente
                    created_by=request.user,
                    updated_by=request.user
                )
        
        messages.success(request, 'Checklist iniciado com sucesso!')
        return redirect('checklist_executar_detalhes', checklist_executado_id=checklist_executado.id)
    
    # Preparar dados para agrupamento por categoria
    itens_personalizados = checklist.itens_personalizados.filter(ativo=True).order_by('ordem')
    
    # Agrupar por categoria do item padrão
    categorias_agrupadas = {}
    for item_personalizado in itens_personalizados:
        try:
            categoria = item_personalizado.item_padrao.categoria if item_personalizado.item_padrao else None
            if categoria:
                if categoria.id not in categorias_agrupadas:
                    categorias_agrupadas[categoria.id] = {
                        'categoria': categoria,
                        'itens': []
                    }
                categorias_agrupadas[categoria.id]['itens'].append(item_personalizado)
        except Exception as e:
            # Log do erro para debug
            print(f"Erro ao processar item personalizado {item_personalizado.id}: {e}")
            continue
    
    # Ordenar categorias pela ordem
    categorias_ordenadas = sorted(categorias_agrupadas.values(), key=lambda x: x['categoria'].ordem) if categorias_agrupadas else []
    
    context = {
        'checklist': checklist,
        'itens_personalizados': itens_personalizados,
        'categorias_agrupadas': categorias_ordenadas,
        'veiculos': Veiculo.objects.all().order_by('marca', 'modelo'),
    }
    return render(request, 'checklist/executar.html', context)

@login_required
def checklist_executar_detalhes(request, checklist_executado_id):
    """Detalhes da execução de um checklist"""
    checklist_executado = get_object_or_404(ChecklistExecutado, id=checklist_executado_id)
    
    # Verificar permissões
    if not request.user.is_staff:
        if request.user.is_oficina:
            try:
                oficina = UsuarioOficina.objects.get(usuario=request.user)
                if not oficina or checklist_executado.checklist.oficina != oficina.oficina:
                    messages.error(request, 'Você não tem permissão para acessar esta execução.')
                    return redirect('checklist_lista')
            except:
                messages.error(request, 'Você não possui uma oficina associada.')
                return redirect('checklist_lista')
        elif request.user.is_profissional:
            profissional = get_object_or_404(Profissional, usuario=request.user)
            if checklist_executado.checklist.oficina != profissional.oficina:
                messages.error(request, 'Você não tem permissão para acessar esta execução.')
                return redirect('checklist_lista')
    
    if request.method == 'POST':
        # Atualizar itens executados
        for item_executado in checklist_executado.itens_executados.all():
            item_id = str(item_executado.id)
            checked = request.POST.get(f'checked_{item_id}') == 'on'
            resultado = request.POST.get(f'resultado_{item_id}', '4')  # '4' = Pendente
            observacoes = request.POST.get(f'observacoes_{item_id}', '')
            
            item_executado.checked = checked
            item_executado.resultado = resultado
            item_executado.observacoes = observacoes
            item_executado.save()
        
        # Atualizar status do checklist com validação rigorosa
        status = request.POST.get('status', 'pendente')
        observacoes_gerais = request.POST.get('observacoes_gerais', '')
        
        # VALIDAÇÃO CRÍTICA: Impedir status "executado" com pendências
        if status == 'executado':
            # Contar itens pendentes (resultado '4', vazio ou nulo)
            itens_pendentes = checklist_executado.itens_executados.filter(
                Q(resultado='4') | Q(resultado='') | Q(resultado__isnull=True)
            ).count()
            
            if itens_pendentes > 0:
                messages.error(
                    request, 
                    f'ERRO: Não é possível marcar como executado! '
                    f'Ainda há {itens_pendentes} item(ns) pendente(s) no checklist. '
                    f'Complete todos os itens antes de finalizar.'
                )
                # Forçar status como pendente
                status = 'pendente'
        
        checklist_executado.status = status
        checklist_executado.observacoes = observacoes_gerais
        checklist_executado.save()
        
        messages.success(request, 'Checklist atualizado com sucesso!')
        return redirect('checklist_executar_detalhes', checklist_executado_id=checklist_executado.id)
    
    # Preparar dados para agrupamento por categoria
    itens_executados = checklist_executado.itens_executados.select_related(
        'item_checklist__item_padrao__categoria'
    ).order_by('item_checklist__ordem')
    
    # Debug: verificar se há itens duplicados
    print(f"Total de itens executados: {itens_executados.count()}")
    item_ids = list(itens_executados.values_list('id', flat=True))
    print(f"IDs dos itens: {item_ids}")
    
    # Agrupar por categoria do item padrão
    categorias_agrupadas = {}
    itens_processados = set()  # Para evitar duplicação
    
    for item_executado in itens_executados:
        try:
            # Verificar se o item já foi processado
            if item_executado.id in itens_processados:
                print(f"Item duplicado encontrado: {item_executado.id}")
                continue
                
            categoria = item_executado.item_checklist.item_padrao.categoria if item_executado.item_checklist.item_padrao else None
            if categoria:
                if categoria.id not in categorias_agrupadas:
                    categorias_agrupadas[categoria.id] = {
                        'categoria': categoria,
                        'itens': []
                    }
                categorias_agrupadas[categoria.id]['itens'].append(item_executado)
                itens_processados.add(item_executado.id)
                print(f"Item {item_executado.id} adicionado à categoria {categoria.nome}")
        except Exception as e:
            # Log do erro para debug
            print(f"Erro ao processar item executado {item_executado.id}: {e}")
            continue
    
    # Ordenar categorias pela ordem
    categorias_ordenadas = sorted(categorias_agrupadas.values(), key=lambda x: x['categoria'].ordem) if categorias_agrupadas else []
    
    context = {
        'checklist_executado': checklist_executado,
        'categorias_agrupadas': categorias_ordenadas,
    }
    return render(request, 'checklist/executar_detalhes.html', context)

@login_required
def checklist_relatorios(request):
    """Relatórios de checklists"""
    if request.user.is_oficina:
        try:
            oficina = UsuarioOficina.objects.get(usuario=request.user)
            if oficina:
                checklists = Checklist.objects.filter(oficina=oficina.oficina)
                executados = ChecklistExecutado.objects.filter(checklist__oficina=oficina.oficina)
            else:
                checklists = Checklist.objects.none()
                executados = ChecklistExecutado.objects.none()
        except:
            checklists = Checklist.objects.none()
            executados = ChecklistExecutado.objects.none()
    elif request.user.is_profissional:
        profissional = get_object_or_404(Profissional, usuario=request.user)
        checklists = Checklist.objects.filter(oficina=profissional.oficina)
        executados = ChecklistExecutado.objects.filter(checklist__oficina=profissional.oficina)
    else:
        checklists = Checklist.objects.filter(ativo=True)
        executados = ChecklistExecutado.objects.all()
    
    # Estatísticas
    total_checklists = checklists.count()
    total_executados = executados.count()
    executados_hoje = executados.filter(data_execucao__date=timezone.now().date()).count()
    pendentes = executados.filter(status='pendente').count()
    
    context = {
        'total_checklists': total_checklists,
        'total_executados': total_executados,
        'executados_hoje': executados_hoje,
        'pendentes': pendentes,
        'executados_recentes': executados.order_by('-data_execucao')[:10],
    }
    return render(request, 'checklist/relatorios.html', context)

def view_checklist_data(request):
    """View temporária para visualizar os dados de checklist populados"""
    categorias = CategoriaChecklist.objects.filter(ativo=True).order_by('ordem')
    total_categorias = categorias.count()
    total_itens = ItemChecklist.objects.filter(ativo=True).count()
    
    # Preparar dados para o template
    categorias_data = []
    for categoria in categorias:
        itens = categoria.itens.filter(ativo=True).order_by('ordem')
        categorias_data.append({
            'categoria': categoria,
            'itens': itens,
            'total_itens': itens.count()
        })
    
    context = {
        'total_categorias': total_categorias,
        'total_itens': total_itens,
        'categorias_data': categorias_data
    }
    
    return render(request, 'checklist/dados_populados.html', context)

@login_required
@oficina_required
def checklist_adicionar_item(request, checklist_id):
    """Adicionar item personalizado ao checklist"""
    checklist = get_object_or_404(Checklist, id=checklist_id)
    
    # Verificar permissões
    if not request.user.is_staff:
        if request.user.is_oficina:
            try:
                oficina = UsuarioOficina.objects.get(usuario=request.user)
                if not oficina or checklist.oficina != oficina.oficina:
                    messages.error(request, 'Você não tem permissão para editar este checklist.')
                    return redirect('checklist_lista')
            except:
                messages.error(request, 'Você não possui uma oficina associada.')
                return redirect('checklist_lista')
        elif request.user.is_profissional:
            profissional = get_object_or_404(Profissional, usuario=request.user)
            if checklist.oficina != profissional.oficina:
                messages.error(request, 'Você não tem permissão para editar este checklist.')
                return redirect('checklist_lista')
    
    if request.method == 'POST':
        categoria_id = request.POST.get('categoria')
        item_padrao_id = request.POST.get('item_padrao')
        nome_personalizado = request.POST.get('nome_personalizado')
        descricao_personalizada = request.POST.get('descricao_personalizada')
        obrigatorio = request.POST.get('obrigatorio') == 'on'
        
        if categoria_id and (item_padrao_id or nome_personalizado):
            categoria = get_object_or_404(CategoriaChecklist, id=categoria_id)
            
            # Determinar a próxima ordem
            ultima_ordem = ItemChecklistPersonalizado.objects.filter(
                checklist=checklist,
                categoria=categoria
            ).aggregate(max_ordem=Sum('ordem'))['max_ordem'] or 0
            
            item_personalizado = ItemChecklistPersonalizado.objects.create(
                checklist=checklist,
                categoria=categoria,
                item_padrao_id=item_padrao_id if item_padrao_id else None,
                nome_personalizado=nome_personalizado,
                descricao_personalizada=descricao_personalizada,
                obrigatorio=obrigatorio,
                ordem=ultima_ordem + 1,
                created_by=request.user,
                updated_by=request.user
            )
            
            messages.success(request, 'Item adicionado ao checklist com sucesso!')
            return redirect('checklist_detalhes', checklist_id=checklist.id)
        else:
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
    
    context = {
        'checklist': checklist,
        'categorias': CategoriaChecklist.objects.filter(ativo=True).order_by('ordem'),
        'itens_padrao': ItemChecklist.objects.filter(ativo=True).order_by('categoria__ordem', 'ordem'),
    }
    
    return render(request, 'checklist/adicionar_item.html', context)

@login_required
@oficina_required
def checklist_gerenciar(request):
    """Página de gerenciamento avançado de checklists para oficinas"""
    try:
        oficina = UsuarioOficina.objects.get(usuario=request.user)
        if not oficina:
            messages.error(request, 'Você não possui uma oficina associada.')
            return redirect('checklist_lista')
    except:
        messages.error(request, 'Você não possui uma oficina associada.')
        return redirect('checklist_lista')
    
    # Filtros
    tipo_veiculo_id = request.GET.get('tipo_veiculo')
    status = request.GET.get('status')
    busca = request.GET.get('busca')
    
    # Query base
    checklists = Checklist.objects.filter(oficina=oficina.oficina)
    
    # Aplicar filtros
    if tipo_veiculo_id:
        checklists = checklists.filter(tipo_veiculo_id=tipo_veiculo_id)
    
    if status == 'ativo':
        checklists = checklists.filter(ativo=True)
    elif status == 'inativo':
        checklists = checklists.filter(ativo=False)
    
    if busca:
        checklists = checklists.filter(
            Q(nome__icontains=busca) | 
            Q(descricao__icontains=busca) |
            Q(tipo_veiculo__nome__icontains=busca)
        )
    
    # Ordenar
    checklists = checklists.select_related('tipo_veiculo').prefetch_related(
        'itens_personalizados', 'checklist_executado'
    ).order_by('-data_criacao')
    
    # Estatísticas
    from datetime import datetime, timedelta
    hoje = datetime.now()
    inicio_mes = hoje.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    stats = {
        'total_checklists': Checklist.objects.filter(oficina=oficina.oficina).count(),
        'checklists_ativos': Checklist.objects.filter(oficina=oficina.oficina, ativo=True).count(),
        'execucoes_mes': ChecklistExecutado.objects.filter(
            checklist__oficina=oficina.oficina,
            data_execucao__gte=inicio_mes
        ).count(),
        'tipos_veiculos': TipoVeiculo.objects.filter(
            checklists__oficina=oficina.oficina
        ).distinct().count(),
    }
    
    context = {
        'checklists': checklists,
        'tipos_veiculos': TipoVeiculo.objects.filter(ativo=True),
        'stats': stats,
    }
    
    return render(request, 'checklist/gerenciar.html', context)

@login_required
@oficina_required
def checklist_gerenciar_itens(request, checklist_id):
    """Gerenciar itens do checklist - selecionar itens por categoria"""
    checklist = get_object_or_404(Checklist, id=checklist_id)
    
    # Verificar permissões
    if not request.user.is_staff:
        if request.user.is_oficina:
            try:
                oficina = UsuarioOficina.objects.get(usuario=request.user)
                if not oficina or checklist.oficina != oficina.oficina:
                    messages.error(request, 'Você não tem permissão para editar este checklist.')
                    return redirect('checklist_lista')
            except:
                messages.error(request, 'Você não possui uma oficina associada.')
                return redirect('checklist_lista')
        elif request.user.is_profissional:
            profissional = get_object_or_404(Profissional, usuario=request.user)
            if checklist.oficina != profissional.oficina:
                messages.error(request, 'Você não tem permissão para editar este checklist.')
                return redirect('checklist_lista')
    
    if request.method == 'POST':
        # Processar seleção de itens
        itens_selecionados = request.POST.getlist('itens_selecionados')
        itens_obrigatorios = request.POST.getlist('itens_obrigatorios')
        itens_criticos = request.POST.getlist('itens_criticos')
        
        # Verificar se existem checklists em execução que referenciam itens deste checklist
        checklists_em_execucao = ChecklistExecutado.objects.filter(
            checklist=checklist,
            status__in=['pendente', 'em_andamento']
        ).exists()
        
        if checklists_em_execucao:
            # Se há checklists em execução, identificar itens que estão sendo usados
            itens_em_uso = set()
            for checklist_exec in ChecklistExecutado.objects.filter(
                checklist=checklist,
                status__in=['pendente', 'em_andamento']
            ):
                itens_em_uso.update(
                    checklist_exec.itens_executados.values_list('item_checklist_id', flat=True)
                )
            
            # Desativar itens que não estão mais selecionados mas estão em uso
            itens_para_desativar = ItemChecklistPersonalizado.objects.filter(
                checklist=checklist,
                id__in=itens_em_uso
            ).exclude(
                item_padrao_id__in=itens_selecionados
            )
            
            for item in itens_para_desativar:
                item.ativo = False
                item.updated_by = request.user
                item.save()
            
            # Remover apenas itens que NÃO estão em uso
            ItemChecklistPersonalizado.objects.filter(
                checklist=checklist
            ).exclude(
                id__in=itens_em_uso
            ).delete()
            
            messages.warning(
                request, 
                f'Alguns itens foram mantidos porque existem checklists em execução. '
                f'Itens não utilizados foram removidos e itens em uso foram desativados quando necessário.'
            )
        else:
            # Se não há checklists em execução, pode remover todos os itens
            ItemChecklistPersonalizado.objects.filter(checklist=checklist).delete()
        
        # Adicionar novos itens selecionados
        for i, item_id in enumerate(itens_selecionados):
            item_padrao = get_object_or_404(ItemChecklist, id=item_id)
            obrigatorio = str(item_id) in itens_obrigatorios
            critico = str(item_id) in itens_criticos
            
            # Verificar se o item já existe (pode ter sido desativado)
            item_existente = ItemChecklistPersonalizado.objects.filter(
                checklist=checklist,
                item_padrao=item_padrao
            ).first()
            
            if item_existente:
                # Reativar e atualizar item existente
                item_existente.ativo = True
                item_existente.obrigatorio = obrigatorio
                item_existente.critico = critico
                item_existente.ordem = i + 1
                item_existente.updated_by = request.user
                item_existente.save()
            else:
                # Criar novo item
                ItemChecklistPersonalizado.objects.create(
                    checklist=checklist,
                    item_padrao=item_padrao,
                    obrigatorio=obrigatorio,
                    critico=critico,
                    ordem=i + 1,
                    created_by=request.user,
                    updated_by=request.user
                )
        
        messages.success(request, f'{len(itens_selecionados)} itens adicionados ao checklist com sucesso!')
        return redirect('checklist_detalhes', checklist_id=checklist.id)
    
    # Buscar itens organizados por categoria
    categorias = CategoriaChecklist.objects.filter(
        ativo=True,
        itens__ativo=True
    ).prefetch_related(
        'itens'
    ).distinct().order_by('ordem')
    
    # Buscar itens já selecionados no checklist
    itens_selecionados = set()
    itens_obrigatorios = set()
    itens_criticos = set()
    
    for item_personalizado in ItemChecklistPersonalizado.objects.filter(
        checklist=checklist,
        item_padrao__isnull=False
    ):
        itens_selecionados.add(item_personalizado.item_padrao_id)
        if item_personalizado.obrigatorio:
            itens_obrigatorios.add(item_personalizado.item_padrao_id)
        if item_personalizado.critico:
            itens_criticos.add(item_personalizado.item_padrao_id)
    
    context = {
        'checklist': checklist,
        'categorias': categorias,
        'itens_selecionados': itens_selecionados,
        'itens_obrigatorios': itens_obrigatorios,
        'itens_criticos': itens_criticos,
    }
    
    return render(request, 'checklist/gerenciar_itens.html', context)

@login_required
def checklist_gerar_pdf(request, checklist_executado_id):
    """Gerar PDF do relatório de checklist executado"""
    checklist_executado = get_object_or_404(ChecklistExecutado, id=checklist_executado_id)
    
    # Verificar se o usuário tem permissão para acessar este checklist
    if not request.user.is_staff:
        if request.user.is_oficina:
            # Oficina só pode ver seus próprios checklists
            try:
                oficina_rel = UsuarioOficina.objects.get(usuario=request.user)
                if checklist_executado.checklist.oficina != oficina_rel.oficina:
                    messages.error(request, 'Você não tem permissão para acessar este checklist.')
                    return redirect('checklist_lista')
            except UsuarioOficina.DoesNotExist:
                messages.error(request, 'Você não possui uma oficina associada.')
                return redirect('checklist_lista')
        elif request.user.is_profissional:
            # Profissionais só podem ver checklists da oficina onde trabalham
            try:
                profissional = Profissional.objects.get(usuario=request.user)
                if checklist_executado.checklist.oficina != profissional.oficina:
                    messages.error(request, 'Você não tem permissão para acessar este checklist.')
                    return redirect('checklist_lista')
            except Profissional.DoesNotExist:
                messages.error(request, 'Você não possui um perfil profissional associado.')
                return redirect('checklist_lista')
        else:
            # Usuários comuns só podem ver checklists de seus veículos
            if checklist_executado.veiculo and checklist_executado.veiculo.usuario != request.user:
                messages.error(request, 'Você não tem permissão para acessar este checklist.')
                return redirect('checklist_lista')
    
    # Verificar se o checklist está executado
    if checklist_executado.status != 'executado':
        messages.error(request, 'PDF disponível apenas para execuções concluídas.')
        return redirect('checklist_detalhes', checklist_id=checklist_executado.checklist.id)
    
    # Buscar itens executados organizados por categoria
    itens_executados = ItemChecklistExecutado.objects.filter(
        checklist_executado=checklist_executado
    ).select_related(
        'item_checklist__item_padrao__categoria',
        'item_checklist'
    ).order_by(
        'item_checklist__item_padrao__categoria__ordem',
        'item_checklist__ordem'
    )
    
    # Organizar itens por categoria
    categorias_data = {}
    for item_executado in itens_executados:
        categoria = item_executado.item_checklist.item_padrao.categoria if item_executado.item_checklist.item_padrao else None
        categoria_nome = categoria.nome if categoria else 'Itens Personalizados'
        
        if categoria_nome not in categorias_data:
            categorias_data[categoria_nome] = []
        
        categorias_data[categoria_nome].append(item_executado)
    
    # Criar PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=20,
        alignment=1  # Center
    )
    
    form_header_style = ParagraphStyle(
        'FormHeader',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=15,
        textColor=colors.darkblue,
        alignment=1
    )
    
    # Conteúdo do PDF
    story = []
    
    # Título
    story.append(Paragraph(f"RELATÓRIO DE CHECKLIST VEICULAR", title_style))
    story.append(Spacer(1, 15))
    
    # Cabeçalho em formato de formulário
    story.append(Paragraph("INFORMAÇÕES GERAIS", form_header_style))
    
    # Primeira linha do formulário - 3 colunas
    form_data_1 = [
        ['Checklist:', checklist_executado.checklist.nome, 'Data/Hora:', checklist_executado.data_execucao.strftime('%d/%m/%Y %H:%M'), 'Status:', checklist_executado.get_status_display()]
    ]
    
    form_table_1 = Table(form_data_1, colWidths=[0.8*inch, 2.2*inch, 0.8*inch, 1.5*inch, 0.6*inch, 1.1*inch])
    form_table_1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTNAME', (4, 0), (4, -1), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(form_table_1)
    story.append(Spacer(1, 8))
    
    # Segunda linha do formulário - 2 colunas
    form_data_2 = [
        ['Oficina:', checklist_executado.checklist.oficina.nome, 'Tipo de Veículo:', checklist_executado.checklist.tipo_veiculo.nome]
    ]
    
    form_table_2 = Table(form_data_2, colWidths=[0.8*inch, 3*inch, 1.2*inch, 2*inch])
    form_table_2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(form_table_2)
    story.append(Spacer(1, 8))
    
    # Terceira linha - Executado por
    form_data_3 = [
        ['Executado por:', checklist_executado.usuario.get_full_name() or checklist_executado.usuario.username, '', '']
    ]
    
    form_table_3 = Table(form_data_3, colWidths=[1.2*inch, 5.8*inch, 0*inch, 0*inch])
    form_table_3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(form_table_3)
    story.append(Spacer(1, 15))
    
    # Seção do veículo (se disponível)
    if checklist_executado.veiculo:
        story.append(Paragraph("DADOS DO VEÍCULO", form_header_style))
        
        # Primeira linha do veículo - 3 colunas
        veiculo_data_1 = [
            ['Marca/Modelo:', f"{checklist_executado.veiculo.marca} {checklist_executado.veiculo.modelo}", 'Placa:', checklist_executado.veiculo.placa, 'Ano:', str(checklist_executado.veiculo.ano)]
        ]
        
        veiculo_table_1 = Table(veiculo_data_1, colWidths=[1.2*inch, 2.3*inch, 0.6*inch, 1.2*inch, 0.5*inch, 1.2*inch])
        veiculo_table_1.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTNAME', (4, 0), (4, -1), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(veiculo_table_1)
        story.append(Spacer(1, 8))
        
        # Segunda linha do veículo - Proprietário
        veiculo_data_2 = [
            ['Proprietário:', checklist_executado.veiculo.usuario.get_full_name() or checklist_executado.veiculo.usuario.username, '', '']
        ]
        
        veiculo_table_2 = Table(veiculo_data_2, colWidths=[1.2*inch, 5.8*inch, 0*inch, 0*inch])
        veiculo_table_2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.beige),
            ('GRID', (0, 0), (1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(veiculo_table_2)
        story.append(Spacer(1, 20))
    
    # Itens por categoria
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.darkblue
    )
    
    # Calcular totalizadores
    total_itens = 0
    total_ok = 0
    total_atencao = 0
    total_problemas = 0
    
    for categoria_nome, itens in categorias_data.items():
        for item_executado in itens:
            total_itens += 1
            resultado = item_executado.resultado or ''
            
            if resultado.lower() in ['ok', 'aprovado', 'conforme', 'sim']:
                total_ok += 1
            elif resultado.lower() in ['atenção', 'atencao', 'revisar', 'verificar']:
                total_atencao += 1
            elif resultado.lower() in ['problema', 'reprovado', 'não conforme', 'nao conforme', 'não', 'nao']:
                total_problemas += 1
    
    # Cards de totalizadores
    story.append(Paragraph("RESUMO DA INSPEÇÃO", heading_style))
    
    # Criar tabela com 4 cards em uma linha
    cards_data = [[
        f"Total de Itens\n{total_itens}",
        f"Itens OK\n{total_ok}", 
        f"Itens com Atenção\n{total_atencao}",
        f"Itens com Problemas\n{total_problemas}"
    ]]
    
    cards_table = Table(cards_data, colWidths=[1.75*inch, 1.75*inch, 1.75*inch, 1.75*inch])
    cards_table.setStyle(TableStyle([
        # Card 1 - Total (azul)
        ('BACKGROUND', (0, 0), (0, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (0, 0), colors.darkblue),
        
        # Card 2 - OK (verde)
        ('BACKGROUND', (1, 0), (1, 0), colors.lightgreen),
        ('TEXTCOLOR', (1, 0), (1, 0), colors.darkgreen),
        
        # Card 3 - Atenção (amarelo)
        ('BACKGROUND', (2, 0), (2, 0), colors.lightyellow),
        ('TEXTCOLOR', (2, 0), (2, 0), colors.orange),
        
        # Card 4 - Problemas (vermelho)
        ('BACKGROUND', (3, 0), (3, 0), colors.lightcoral),
        ('TEXTCOLOR', (3, 0), (3, 0), colors.red),
        
        # Estilo geral
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 2, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    
    story.append(cards_table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("ITENS VERIFICADOS", heading_style))
    
    for categoria_nome, itens in categorias_data.items():
        # Título da categoria
        story.append(Paragraph(f"Categoria: {categoria_nome}", ParagraphStyle(
            'CategoryTitle',
            parent=styles['Heading3'],
            fontSize=12,
            spaceAfter=10,
            textColor=colors.darkgreen
        )))
        
        # Tabela de itens
        item_data = [['Item', 'Resultado', 'Valor', 'Observações']]
        
        for item_executado in itens:
            item_nome = (
                item_executado.item_checklist.item_padrao.nome 
                if item_executado.item_checklist.item_padrao 
                else item_executado.item_checklist.nome_personalizado or 'Item Personalizado'
            )
            
            resultado = item_executado.resultado or '-'
            valor = item_executado.valor_resultado or '-'
            observacoes = item_executado.observacoes or '-'
            
            # Limitar o tamanho das observações
            if len(observacoes) > 50:
                observacoes = observacoes[:47] + '...'
            
            item_data.append([item_nome, resultado, valor, observacoes])
        
        item_table = Table(item_data, colWidths=[2.5*inch, 1*inch, 1*inch, 1.5*inch])
        
        # Estilo base da tabela
        table_style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]
        
        # Adicionar cor vermelha para itens com problemas
        for i, item_executado in enumerate(itens, start=1):
            resultado = item_executado.resultado or ''
            if resultado.lower() in ['problema', 'reprovado', 'não conforme', 'nao conforme', 'não', 'nao']:
                table_style.append(('TEXTCOLOR', (1, i), (1, i), colors.red))  # Coluna Resultado
                table_style.append(('TEXTCOLOR', (2, i), (2, i), colors.red))  # Coluna Valor
        
        item_table.setStyle(TableStyle(table_style))
        
        story.append(item_table)
        story.append(Spacer(1, 20))
    
    # Rodapé
    story.append(Spacer(1, 30))
    story.append(Paragraph(
        f"Relatório gerado em {timezone.now().strftime('%d/%m/%Y às %H:%M')}",
        ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=1  # Center
        )
    ))
    
    # Construir PDF
    doc.build(story)
    
    # Retornar resposta
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="checklist_{checklist_executado.id}_{checklist_executado.data_execucao.strftime("%Y%m%d")}.pdf"'
    
    return response
