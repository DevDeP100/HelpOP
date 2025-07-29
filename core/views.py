from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum, Count, Q
from .models import (
    Usuario, Veiculo, Manutencao, Profissional, Servico,
    TipoVeiculo, CategoriaChecklist, ItemChecklist, Checklist, 
    ItemChecklistPersonalizado, ChecklistExecutado, ItemChecklistExecutado, Arquivos_checklist
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
                messages.warning(request, 'Sua conta está aguardando aprovação do administrador. Você receberá um email quando for aprovado.')
                return redirect('home')
            
            login(request, user)
            messages.success(request, f'Bem-vindo de volta, {user.get_full_name() or user.username}!')
            return redirect('dashboard')
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
                Profissional.objects.create(usuario=user)
            
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
                
                messages.success(request, f'Usuário {user.get_full_name()} aprovado com sucesso!')
                
                # TODO: Enviar email de notificação para o usuário
                
            elif action == 'rejeitar':
                # Deletar o usuário rejeitado
                user.delete()
                messages.success(request, f'Usuário rejeitado e removido do sistema.')
                
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
            oficina = request.user.oficina
            if oficina:
                checklists = Checklist.objects.filter(oficina=oficina)
            else:
                checklists = Checklist.objects.none()
        except:
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
    """Criar novo checklist"""
    if request.method == 'POST':
        # Lógica para criar checklist
        nome = request.POST.get('nome')
        tipo_veiculo_id = request.POST.get('tipo_veiculo')
        descricao = request.POST.get('descricao', '')
        
        if nome and tipo_veiculo_id:
            tipo_veiculo = get_object_or_404(TipoVeiculo, id=tipo_veiculo_id)
            
            # Pegar a oficina diretamente do usuário logado
            try:
                oficina = request.user.oficina
                if not oficina:
                    messages.error(request, 'Você não possui uma oficina associada. Entre em contato com o administrador.')
                    return redirect('checklist_lista')
            except:
                messages.error(request, 'Você não possui uma oficina associada. Entre em contato com o administrador.')
                return redirect('checklist_lista')
            
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
                oficina = request.user.oficina
                if not oficina or checklist.oficina != oficina:
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
    
    context = {
        'checklist': checklist,
        'itens_personalizados': checklist.itens_personalizados.filter(ativo=True).order_by('categoria__ordem', 'ordem'),
        'execucoes': checklist.checklist_executado.all().order_by('-data_execucao')[:5],
    }
    return render(request, 'checklist/detalhes.html', context)

@login_required
@oficina_required
def checklist_editar(request, checklist_id):
    """Editar checklist"""
    checklist = get_object_or_404(Checklist, id=checklist_id)
    
    # Verificar se o usuário tem permissão para editar
    try:
        oficina = request.user.oficina
        if not oficina or checklist.oficina != oficina:
            messages.error(request, 'Você não tem permissão para editar este checklist.')
            return redirect('checklist_lista')
    except:
        messages.error(request, 'Você não possui uma oficina associada.')
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
                oficina = request.user.oficina
                if not oficina or checklist.oficina != oficina:
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
                'itens_personalizados': checklist.itens_personalizados.filter(ativo=True).order_by('categoria__ordem', 'ordem'),
                'veiculos': Veiculo.objects.all().order_by('marca', 'modelo'),
            }
            return render(request, 'checklist/executar.html', context)
        
        veiculo = get_object_or_404(Veiculo, id=veiculo_id)
        
        checklist_executado = ChecklistExecutado.objects.create(
            checklist=checklist,
            veiculo=veiculo,
            usuario=request.user,
            observacoes=observacoes
        )
        
        # Criar itens executados baseados nos itens personalizados
        for item_personalizado in checklist.itens_personalizados.filter(ativo=True):
            ItemChecklistExecutado.objects.create(
                checklist_executado=checklist_executado,
                item_checklist=item_personalizado.item_padrao or item_personalizado,
                resultado='pendente'
            )
        
        messages.success(request, 'Checklist iniciado com sucesso!')
        return redirect('checklist_executar_detalhes', checklist_executado_id=checklist_executado.id)
    
    context = {
        'checklist': checklist,
        'itens_personalizados': checklist.itens_personalizados.filter(ativo=True).order_by('categoria__ordem', 'ordem'),
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
                oficina = request.user.oficina
                if not oficina or checklist_executado.checklist.oficina != oficina:
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
        for item_executado in checklist_executado.itens_checklist_executado.all():
            item_id = str(item_executado.id)
            checked = request.POST.get(f'checked_{item_id}') == 'on'
            resultado = request.POST.get(f'resultado_{item_id}', 'pendente')
            observacoes = request.POST.get(f'observacoes_{item_id}', '')
            
            item_executado.checked = checked
            item_executado.resultado = resultado
            item_executado.observacoes = observacoes
            item_executado.save()
        
        # Atualizar status do checklist
        status = request.POST.get('status', 'pendente')
        observacoes_gerais = request.POST.get('observacoes_gerais', '')
        
        checklist_executado.status = status
        checklist_executado.observacoes = observacoes_gerais
        checklist_executado.save()
        
        messages.success(request, 'Checklist atualizado com sucesso!')
        return redirect('checklist_executar_detalhes', checklist_executado_id=checklist_executado.id)
    
    context = {
        'checklist_executado': checklist_executado,
        'itens_executados': checklist_executado.itens_checklist_executado.all().order_by('item_checklist__categoria__ordem', 'item_checklist__ordem'),
    }
    return render(request, 'checklist/executar_detalhes.html', context)

@login_required
def checklist_relatorios(request):
    """Relatórios de checklists"""
    if request.user.is_oficina:
        try:
            oficina = request.user.oficina
            if oficina:
                checklists = Checklist.objects.filter(oficina=oficina)
                executados = ChecklistExecutado.objects.filter(checklist__oficina=oficina)
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
