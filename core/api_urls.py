from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    UsuarioViewSet, VeiculoViewSet, OficinaViewSet, ProfissionalViewSet,
    ServicoViewSet, ManutencaoViewSet, AvaliacaoViewSet,
    TipoVeiculoViewSet, CategoriaChecklistViewSet, ItemChecklistViewSet,
    ChecklistViewSet, ItemChecklistPersonalizadoViewSet, ChecklistExecutadoViewSet,
    ItemChecklistExecutadoViewSet, ArquivosChecklistViewSet
)
from .auth_views import api_login, api_logout

# Criar router
router = DefaultRouter()

# Registrar ViewSets
router.register(r'usuarios', UsuarioViewSet)
router.register(r'veiculos', VeiculoViewSet, basename='veiculo')
router.register(r'oficinas', OficinaViewSet)
router.register(r'profissionais', ProfissionalViewSet)
router.register(r'servicos', ServicoViewSet)
router.register(r'manutencoes', ManutencaoViewSet, basename='manutencao')
router.register(r'avaliacoes', AvaliacaoViewSet, basename='avaliacao')

# ViewSets para Checklist
router.register(r'tipos-veiculo', TipoVeiculoViewSet)
router.register(r'categorias-checklist', CategoriaChecklistViewSet)
router.register(r'itens-checklist', ItemChecklistViewSet)
router.register(r'checklists', ChecklistViewSet, basename='checklist')
router.register(r'itens-checklist-personalizados', ItemChecklistPersonalizadoViewSet, basename='itemchecklistpersonalizado')
router.register(r'checklists-executados', ChecklistExecutadoViewSet, basename='checklistexecutado')
router.register(r'itens-checklist-executados', ItemChecklistExecutadoViewSet, basename='itemchecklistexecutado')
router.register(r'arquivos-checklist', ArquivosChecklistViewSet, basename='arquivoschecklist')

# URLs da API
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    path('login/', api_login, name='api_login'),
    path('logout/', api_logout, name='api_logout'),
] 