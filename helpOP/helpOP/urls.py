# URL configuration for helpOP project.

from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Páginas principais
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Autenticação
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),
    path('verificar-email/<int:user_id>/', views.verificar_email, name='verificar_email'),
    path('reenviar-codigo/<int:user_id>/', views.reenviar_codigo, name='reenviar_codigo'),
    
    # Perfil do usuário
    path('perfil/', views.perfil, name='perfil'),
    
    # Veículos
    path('veiculos/', views.veiculos, name='veiculos'),
    path('veiculos/adicionar/', views.adicionar_veiculo, name='adicionar_veiculo'),
    path('veiculos/<int:veiculo_id>/', views.veiculo_detalhes, name='veiculo_detalhes'),
    path('veiculos/<int:veiculo_id>/editar/', views.editar_veiculo, name='editar_veiculo'),
    
    # Manutenções
    path('manutencoes/', views.manutencoes, name='manutencoes'),
    path('manutencoes/nova/', views.nova_manutencao, name='nova_manutencao'),
    path('veiculos/<int:veiculo_id>/manutencao/', views.nova_manutencao, name='nova_manutencao_veiculo'),
    
    # Serviços e Profissionais
    path('servicos/', views.servicos, name='servicos'),
    path('profissionais/', views.profissionais, name='profissionais'),
    path('profissionais/buscar/', views.buscar_profissionais, name='buscar_profissionais'),
    
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
] 