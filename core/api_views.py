from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import (
    Usuario, Veiculo, Oficina, Profissional, Servico, Manutencao, Avaliacao,
    TipoVeiculo, CategoriaChecklist, ItemChecklist, Checklist, ItemChecklistPersonalizado,
    ChecklistExecutado, ItemChecklistExecutado, Arquivos_checklist, usuarioOficina
)
from .serializers import (
    UsuarioSerializer, VeiculoSerializer, OficinaSerializer, ProfissionalSerializer,
    ServicoSerializer, ManutencaoSerializer, AvaliacaoSerializer,
    TipoVeiculoSerializer, CategoriaChecklistSerializer, ItemChecklistSerializer,
    ChecklistSerializer, ItemChecklistPersonalizadoSerializer, ChecklistExecutadoSerializer,
    ItemChecklistExecutadoSerializer, ArquivosChecklistSerializer,
    ChecklistDetalhadoSerializer, ChecklistExecutadoDetalhadoSerializer,
    UsuarioOficinaSerializer
)

# Permissões personalizadas
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.usuario == request.user

class IsOficinaOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_oficina

class IsProfissionalOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_profissional or request.user.is_oficina

# ViewSets
class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar usuários do sistema.
    
    Permite criar, listar, atualizar e deletar usuários.
    Apenas administradores podem acessar este endpoint.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAdminUser]
    
    @swagger_auto_schema(
        operation_description="Retorna dados do usuário logado",
        responses={
            200: UsuarioSerializer,
            401: 'Não autorizado',
        }
    )
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Retorna dados do usuário logado"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class VeiculoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar veículos dos usuários.
    
    Permite criar, listar, atualizar e deletar veículos.
    Usuários comuns veem apenas seus próprios veículos.
    Profissionais e oficinas veem todos os veículos.
    """
    serializer_class = VeiculoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Veiculo.objects.all()
        elif self.request.user.is_profissional or self.request.user.is_oficina:
            return Veiculo.objects.all()
        else:
            return Veiculo.objects.filter(usuario=self.request.user)

class OficinaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar oficinas do sistema.
    
    Permite criar, listar, atualizar e deletar oficinas.
    Usuários comuns veem apenas oficinas aprovadas.
    """
    queryset = Oficina.objects.all()
    serializer_class = OficinaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Oficina.objects.all()
        elif self.request.user.is_oficina:
            return Oficina.objects.filter(usuario=self.request.user)
        else:
            return Oficina.objects.filter(aprovado=True)

class ProfissionalViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar profissionais do sistema.
    
    Permite criar, listar, atualizar e deletar profissionais.
    Usuários comuns veem apenas profissionais aprovados.
    """
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Profissional.objects.all()
        else:
            return Profissional.objects.filter(aprovado=True)

class ServicoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar serviços disponíveis.
    
    Permite criar, listar, atualizar e deletar serviços.
    Retorna apenas serviços ativos.
    """
    queryset = Servico.objects.filter(ativo=True)
    serializer_class = ServicoSerializer
    permission_classes = [permissions.IsAuthenticated]

class ManutencaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar manutenções de veículos.
    
    Permite criar, listar, atualizar e deletar manutenções.
    Apenas profissionais e oficinas podem criar manutenções.
    Usuários veem manutenções baseadas em suas permissões.
    """
    serializer_class = ManutencaoSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfissionalOrReadOnly]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Manutencao.objects.all()
        elif self.request.user.is_profissional or self.request.user.is_oficina:
            return Manutencao.objects.filter(profissional__usuario=self.request.user)
        else:
            return Manutencao.objects.filter(veiculo__usuario=self.request.user)

class AvaliacaoViewSet(viewsets.ModelViewSet):
    serializer_class = AvaliacaoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Avaliacao.objects.all()
        else:
            return Avaliacao.objects.filter(profissional__aprovado=True)

# ViewSets para o sistema de Checklist
class TipoVeiculoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar tipos de veículos.
    
    Permite criar, listar, atualizar e deletar tipos de veículos.
    Retorna apenas tipos ativos.
    """
    queryset = TipoVeiculo.objects.filter(ativo=True)
    serializer_class = TipoVeiculoSerializer
    permission_classes = [permissions.IsAuthenticated]

class CategoriaChecklistViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar categorias de checklist.
    
    Permite criar, listar, atualizar e deletar categorias.
    Retorna apenas categorias ativas, ordenadas por ordem.
    """
    queryset = CategoriaChecklist.objects.filter(ativo=True).order_by('ordem')
    serializer_class = CategoriaChecklistSerializer
    permission_classes = [permissions.IsAuthenticated]

class ItemChecklistViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar itens de checklist.
    
    Permite criar, listar, atualizar e deletar itens de checklist.
    Retorna apenas itens ativos, ordenados por categoria e ordem.
    """
    queryset = ItemChecklist.objects.filter(ativo=True).order_by('ordem')
    serializer_class = ItemChecklistSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChecklistViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar checklists do sistema.
    
    Permite criar, listar, atualizar e deletar checklists.
    Apenas oficinas podem criar e editar checklists.
    Usuários comuns veem apenas checklists ativos.
    """
    serializer_class = ChecklistSerializer
    permission_classes = [permissions.IsAuthenticated, IsOficinaOrReadOnly]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Checklist.objects.all()
        elif self.request.user.is_oficina:
            try:
                oficina = self.request.user.oficina
                if oficina:
                    return Checklist.objects.filter(oficina=oficina)
                else:
                    return Checklist.objects.none()
            except:
                return Checklist.objects.none()
        elif self.request.user.is_profissional:
            profissional = get_object_or_404(Profissional, usuario=self.request.user)
            return Checklist.objects.filter(oficina=profissional.oficina)
        else:
            return Checklist.objects.filter(ativo=True)
    
    @swagger_auto_schema(
        operation_description="Retorna checklist com todos os detalhes incluindo itens e execuções",
        responses={
            200: ChecklistDetalhadoSerializer,
            404: 'Checklist não encontrado',
        }
    )
    @action(detail=True, methods=['get'])
    def detalhado(self, request, pk=None):
        """Retorna checklist com todos os detalhes"""
        checklist = self.get_object()
        serializer = ChecklistDetalhadoSerializer(checklist)
        return Response(serializer.data)

class ItemChecklistPersonalizadoViewSet(viewsets.ModelViewSet):
    serializer_class = ItemChecklistPersonalizadoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOficinaOrReadOnly]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return ItemChecklistPersonalizado.objects.all()
        elif self.request.user.is_oficina:
            try:
                oficina = self.request.user.oficina
                if oficina:
                    return ItemChecklistPersonalizado.objects.filter(checklist__oficina=oficina)
                else:
                    return ItemChecklistPersonalizado.objects.none()
            except:
                return ItemChecklistPersonalizado.objects.none()
        else:
            return ItemChecklistPersonalizado.objects.filter(ativo=True)

class ChecklistExecutadoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar execuções de checklists.
    
    Permite criar, listar, atualizar e deletar execuções de checklists.
    Usuários veem execuções baseadas em suas permissões.
    """
    serializer_class = ChecklistExecutadoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return ChecklistExecutado.objects.all()
        elif self.request.user.is_oficina:
            try:
                oficina = self.request.user.oficina
                if oficina:
                    return ChecklistExecutado.objects.filter(checklist__oficina=oficina)
                else:
                    return ChecklistExecutado.objects.none()
            except:
                return ChecklistExecutado.objects.none()
        elif self.request.user.is_profissional:
            profissional = get_object_or_404(Profissional, usuario=self.request.user)
            return ChecklistExecutado.objects.filter(checklist__oficina=profissional.oficina)
        else:
            return ChecklistExecutado.objects.all()
    
    @swagger_auto_schema(
        operation_description="Retorna execução de checklist com todos os detalhes incluindo itens executados",
        responses={
            200: ChecklistExecutadoDetalhadoSerializer,
            404: 'Execução não encontrada',
        }
    )
    @action(detail=True, methods=['get'])
    def detalhado(self, request, pk=None):
        """Retorna checklist executado com todos os detalhes"""
        checklist_executado = self.get_object()
        serializer = ChecklistExecutadoDetalhadoSerializer(checklist_executado)
        return Response(serializer.data)

class ItemChecklistExecutadoViewSet(viewsets.ModelViewSet):
    serializer_class = ItemChecklistExecutadoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return ItemChecklistExecutado.objects.all()
        elif self.request.user.is_oficina:
            try:
                oficina = self.request.user.oficina
                if oficina:
                    return ItemChecklistExecutado.objects.filter(checklist_executado__checklist__oficina=oficina)
                else:
                    return ItemChecklistExecutado.objects.none()
            except:
                return ItemChecklistExecutado.objects.none()
        elif self.request.user.is_profissional:
            profissional = get_object_or_404(Profissional, usuario=self.request.user)
            return ItemChecklistExecutado.objects.filter(checklist_executado__checklist__oficina=profissional.oficina)
        else:
            return ItemChecklistExecutado.objects.all()

class ArquivosChecklistViewSet(viewsets.ModelViewSet):
    serializer_class = ArquivosChecklistSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Arquivos_checklist.objects.all()
        elif self.request.user.is_oficina:
            try:
                oficina = self.request.user.oficina
                if oficina:
                    return Arquivos_checklist.objects.filter(item_checklist_executado__checklist_executado__checklist__oficina=oficina)
                else:
                    return Arquivos_checklist.objects.none()
            except:
                return Arquivos_checklist.objects.none()
        elif self.request.user.is_profissional:
            profissional = get_object_or_404(Profissional, usuario=self.request.user)
            return Arquivos_checklist.objects.filter(item_checklist_executado__checklist_executado__checklist__oficina=profissional.oficina)
        else:
            return Arquivos_checklist.objects.all() 

class UsuarioOficinaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar relacionamentos entre usuários e oficinas.
    
    Permite criar, listar, atualizar e deletar relacionamentos usuário-oficina.
    Usuários veem apenas seus próprios relacionamentos.
    Administradores veem todos os relacionamentos.
    """
    serializer_class = UsuarioOficinaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return usuarioOficina.objects.all()
        elif self.request.user.is_oficina:
            try:
                oficina = self.request.user.oficina
                if oficina:
                    # Usuário tem oficina direta - pode ver relacionamentos da sua oficina
                    return usuarioOficina.objects.filter(oficina=oficina)
                else:
                    # Usuário é oficina mas não tem oficina direta - pode ver seus próprios relacionamentos
                    return usuarioOficina.objects.filter(usuario=self.request.user)
            except:
                # Usuário é oficina mas não tem oficina direta - pode ver seus próprios relacionamentos
                return usuarioOficina.objects.filter(usuario=self.request.user)
        else:
            return usuarioOficina.objects.filter(usuario=self.request.user)
    
    @swagger_auto_schema(
        operation_description="Retorna relacionamentos usuário-oficina ativos",
        responses={
            200: UsuarioOficinaSerializer(many=True),
            401: 'Não autorizado',
        }
    )
    @action(detail=False, methods=['get'])
    def ativos(self, request):
        """Retorna apenas relacionamentos ativos"""
        queryset = self.get_queryset().filter(ativo=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Retorna relacionamentos por oficina específica",
        manual_parameters=[
            openapi.Parameter(
                'oficina_id',
                openapi.IN_QUERY,
                description="ID da oficina",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: UsuarioOficinaSerializer(many=True),
            400: 'ID da oficina não fornecido',
        }
    )
    @action(detail=False, methods=['get'])
    def por_oficina(self, request):
        """Retorna relacionamentos por oficina específica"""
        oficina_id = request.query_params.get('oficina_id')
        if not oficina_id:
            return Response(
                {'error': 'ID da oficina é obrigatório'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(oficina_id=oficina_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data) 