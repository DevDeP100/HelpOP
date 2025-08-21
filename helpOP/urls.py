# URL configuration for helpOP project.

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuração do Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="HelpOP API",
        default_version='v1',
        description="API REST completa para o sistema HelpOP - Plataforma de serviços automotivos",
        terms_of_service="https://www.helpop.com.br/terms/",
        contact=openapi.Contact(email="contato@helpop.com.br"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Swagger URLs
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # URLs da aplicação
    path('', views.home, name='home'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('veiculos/', views.veiculos, name='veiculos'),
    path('veiculos/adicionar/', views.adicionar_veiculo, name='adicionar_veiculo'),
    path('veiculos/<int:veiculo_id>/', views.veiculo_detalhes, name='veiculo_detalhes'),
    path('veiculos/<int:veiculo_id>/editar/', views.editar_veiculo, name='editar_veiculo'),
    path('veiculos/<int:veiculo_id>/nova-manutencao/', views.nova_manutencao, name='nova_manutencao_veiculo'),
    path('manutencoes/adicionar/', views.nova_manutencao, name='nova_manutencao'),
    path('manutencoes/', views.manutencoes, name='manutencoes'),
    path('servicos/', views.servicos, name='servicos'),
    path('profissionais/', views.profissionais, name='profissionais'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('verificar-email/<int:user_id>/', views.verificar_email, name='verificar_email'),
    path('reenviar-codigo/<int:user_id>/', views.reenviar_codigo, name='reenviar_codigo'),
    # Administração
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/usuario/<int:user_id>/', views.admin_usuario_detalhes, name='admin_usuario_detalhes'),
    path('admin-panel/aprovar-usuarios/', views.admin_aprovar_usuarios, name='admin_aprovar_usuarios'),
    path('admin-panel/gerenciar-usuarios/', views.admin_gerenciar_usuarios, name='admin_gerenciar_usuarios'),
    # Profissionais e Oficinas
    path('profissional/dashboard/', views.profissional_dashboard, name='profissional_dashboard'),
    path('profissional/manutencoes/', views.profissional_manutencoes, name='profissional_manutencoes'),
    path('profissional/nova-manutencao/', views.profissional_nova_manutencao, name='profissional_nova_manutencao'),
    path('profissional/editar-manutencao/<int:manutencao_id>/', views.profissional_editar_manutencao, name='profissional_editar_manutencao'),
    # Checklist
    path('checklist/', views.checklist_lista, name='checklist_lista'),
    path('checklist/gerenciar/', views.checklist_gerenciar, name='checklist_gerenciar'),
    path('checklist/dados-populados/', views.view_checklist_data, name='view_checklist_data'),
    path('checklist/criar/', views.checklist_criar, name='checklist_criar'),
    path('checklist/<int:checklist_id>/', views.checklist_detalhes, name='checklist_detalhes'),
    path('checklist/<int:checklist_id>/editar/', views.checklist_editar, name='checklist_editar'),
    path('checklist/<int:checklist_id>/executar/', views.checklist_executar, name='checklist_executar'),
    path('checklist/executar/<int:checklist_executado_id>/', views.checklist_executar_detalhes, name='checklist_executar_detalhes'),
    path('checklist/relatorios/', views.checklist_relatorios, name='checklist_relatorios'),
    # API URLs
    path('api/', include('core.api_urls')),
]

# Adicionar URLs para arquivos estáticos em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    # Adicionar URL específica para o logo
    urlpatterns += static('static/images/', document_root=settings.BASE_DIR / 'static' / 'images')