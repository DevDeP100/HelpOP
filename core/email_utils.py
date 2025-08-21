from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .models import CodigoVerificacao
import os
from pathlib import Path
import base64

def enviar_codigo_verificacao(usuario):
    """
    Envia código de verificação por email
    """
    # Criar ou obter código de verificação
    codigo_obj, created = CodigoVerificacao.objects.get_or_create(
        usuario=usuario,
        usado=False
    )
    
    if not created:
        # Se já existe um código válido, usar ele
        if codigo_obj.valido():
            codigo = codigo_obj.codigo
        else:
            # Se expirou, gerar novo código
            codigo_obj.delete()
            codigo_obj = CodigoVerificacao.objects.create(usuario=usuario)
            codigo = codigo_obj.codigo
    else:
        codigo = codigo_obj.codigo
    
    # Preparar email
    assunto = 'Verificação de Email - HelpOP'
    
    # Carregar e converter a imagem para base64
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'ChatGPT Image 28_07_2025, 23_09_31.png')
    with open(logo_path, 'rb') as f:
        logo_data = f.read()
    logo_base64 = base64.b64encode(logo_data).decode('utf-8')
    
    # Template HTML para o email
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Verificação de Email - HelpOP</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                line-height: 1.6; 
                color: #333; 
                background: #f5f5f5;
                padding: 20px;
            }}
            .email-container {{ 
                max-width: 600px; 
                margin: 0 auto; 
                background: white;
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}
            .header {{ 
                background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); 
                color: white; 
                padding: 30px 20px; 
                text-align: center; 
                position: relative;
            }}
            .logo-container {{
                display: inline-block;
                width: 80px;
                height: 80px;
                background: #ffd700;
                border-radius: 50%;
                margin-bottom: 15px;
                text-align: center;
                vertical-align: middle;
                border: 3px solid white;
                box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
            }}
            .logo-image {{
                width: 100%;
                height: 100%;
                object-fit: contain;
                display: block;
                margin: 0 auto;
                border-radius: 50%;
                border: 3px solid white;
                box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
            }}
            .header h1 {{
                font-size: 28px;
                margin-bottom: 5px;
                color: #ffd700;
                font-weight: bold;
            }}
            .header p {{
                font-size: 16px;
                opacity: 0.9;
            }}
            .content {{ 
                padding: 40px 30px; 
                background: white;
            }}
            .welcome-text {{
                font-size: 18px;
                color: #1a1a1a;
                margin-bottom: 20px;
                font-weight: 500;
            }}
            .description {{
                color: #666;
                margin-bottom: 30px;
                font-size: 16px;
            }}
            .codigo-container {{
                background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
                padding: 25px;
                border-radius: 12px;
                text-align: center;
                margin: 30px 0;
                border: 2px solid #1a1a1a;
                box-shadow: 0 5px 20px rgba(255, 215, 0, 0.2);
            }}
            .codigo {{
                font-size: 32px;
                font-weight: bold;
                color: #000000;
                letter-spacing: 8px;
                font-family: 'Courier New', monospace;
                text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .expiry-notice {{
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                color: #856404;
                padding: 15px;
                border-radius: 8px;
                margin: 20px 0;
                font-size: 14px;
            }}
            .warning {{
                background: #f8d7da;
                border: 1px solid #f5c6cb;
                color: #721c24;
                padding: 15px;
                border-radius: 8px;
                margin: 20px 0;
                font-size: 14px;
            }}
            .footer {{ 
                background: #1a1a1a;
                color: white;
                padding: 25px 30px; 
                text-align: center;
                font-size: 14px;
            }}
            .footer p {{
                margin-bottom: 10px;
            }}
            .social-links {{
                margin-top: 15px;
            }}
            .social-links a {{
                color: #ffd700;
                text-decoration: none;
                margin: 0 10px;
                font-weight: bold;
            }}
            .signature {{
                margin-top: 25px;
                padding-top: 20px;
                border-top: 1px solid #eee;
                color: #666;
            }}
            @media (max-width: 600px) {{
                .email-container {{
                    margin: 10px;
                    border-radius: 10px;
                }}
                .content {{
                    padding: 30px 20px;
                }}
                .codigo {{
                    font-size: 24px;
                    letter-spacing: 4px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <div class="logo-container">
                    <img src="data:image/png;base64,{logo_base64}" alt="HelpOP Logo" class="logo-image">
                </div>
                <p>Sua plataforma completa para serviços automotivos</p>
            </div>
            
            <div class="content">
                <div class="welcome-text">
                    Olá, <strong>{usuario.first_name or usuario.username}</strong>! 👋
                </div>
                
                <div class="description">
                    Bem-vindo ao HelpOP! Para completar seu cadastro e começar a usar nossa plataforma, 
                    use o código de verificação abaixo:
                </div>
                
                <div class="codigo-container">
                    <div class="codigo">{codigo}</div>
                </div>
                
                <div class="expiry-notice">
                    ⏰ <strong>Este código expira em 24 horas.</strong>
                </div>
                
                <div class="warning">
                    ⚠️ Se você não solicitou este cadastro, ignore este email.
                </div>
                
                <div class="signature">
                    <p>Atenciosamente,<br>
                    <strong>Equipe HelpOP</strong></p>
                </div>
            </div>
            
            <div class="footer">
                <p><strong>HelpOP</strong></p>
                <p>Sua plataforma de serviços automotivos</p>
                <div class="social-links">
                    <a href="#">Website</a> | 
                    <a href="#">Suporte</a> | 
                    <a href="#">Contato</a>
                </div>
                <p style="margin-top: 15px; font-size: 12px; opacity: 0.7;">
                    © 2024 HelpOP. Todos os direitos reservados.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Mensagem de texto simples (fallback)
    mensagem_texto = f"""
    Olá {usuario.first_name or usuario.username}!
    
    Bem-vindo ao HelpOP! Para completar seu cadastro, use o código de verificação abaixo:
    
    CÓDIGO: {codigo}
    
    Este código expira em 24 horas.
    
    Se você não solicitou este cadastro, ignore este email.
    
    Atenciosamente,
    Equipe HelpOP
    """
    
    # Enviar email
    try:
        send_mail(
            subject=assunto,
            message=mensagem_texto,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[usuario.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False

def verificar_codigo(usuario, codigo_digitado):
    """
    Verifica se o código digitado é válido
    """
    try:
        codigo_obj = CodigoVerificacao.objects.get(
            usuario=usuario,
            codigo=codigo_digitado,
            usado=False
        )
        
        if codigo_obj.valido():
            # Marcar código como usado
            codigo_obj.usado = True
            codigo_obj.save()
            
            # Marcar usuário como verificado
            usuario.email_verificado = True
            usuario.save()
            
            return True
        else:
            return False
    except CodigoVerificacao.DoesNotExist:
        return False

def enviar_email_aprovacao(usuario):
    """
    Envia email de aprovação para profissional/oficina
    """
    # Carregar logo
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'ChatGPT Image 28_07_2025, 23_09_31.png')
    with open(logo_path, 'rb') as f:
        logo_data = f.read()
    logo_base64 = base64.b64encode(logo_data).decode('utf-8')
    
    tipo_usuario = "Profissional" if usuario.is_profissional else "Oficina"
    assunto = f'🎉 Conta Aprovada - HelpOP {tipo_usuario}'
    
    # Template HTML para aprovação
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Conta Aprovada - HelpOP</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                line-height: 1.6; 
                color: #333; 
                background: #f5f5f5;
                padding: 20px;
            }}
            .email-container {{ 
                max-width: 600px; 
                margin: 0 auto; 
                background: white;
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}
            .header {{ 
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                color: white; 
                padding: 30px 20px; 
                text-align: center; 
            }}
            .logo-container {{
                display: inline-block;
                width: 80px;
                height: 80px;
                background: #ffd700;
                border-radius: 50%;
                margin-bottom: 15px;
                border: 3px solid white;
                box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
            }}
            .logo-image {{
                width: 100%;
                height: 100%;
                object-fit: contain;
                border-radius: 50%;
            }}
            .header h1 {{
                font-size: 28px;
                margin-bottom: 5px;
                color: white;
                font-weight: bold;
            }}
            .content {{ 
                padding: 40px 30px; 
                background: white;
            }}
            .success-icon {{
                text-align: center;
                font-size: 60px;
                margin-bottom: 20px;
            }}
            .welcome-text {{
                font-size: 18px;
                color: #1a1a1a;
                margin-bottom: 20px;
                font-weight: 500;
                text-align: center;
            }}
            .description {{
                color: #666;
                margin-bottom: 30px;
                font-size: 16px;
                text-align: center;
            }}
            .button-container {{
                text-align: center;
                margin: 30px 0;
            }}
            .login-button {{
                display: inline-block;
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 16px;
                box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
            }}
            .benefits {{
                background: #f8f9fa;
                border-left: 4px solid #28a745;
                padding: 20px;
                margin: 20px 0;
                border-radius: 0 8px 8px 0;
            }}
            .benefits h3 {{
                color: #28a745;
                margin-bottom: 10px;
            }}
            .benefits ul {{
                list-style: none;
                padding: 0;
            }}
            .benefits li {{
                margin: 8px 0;
                padding-left: 20px;
                position: relative;
            }}
            .benefits li::before {{
                content: "✓";
                position: absolute;
                left: 0;
                color: #28a745;
                font-weight: bold;
            }}
            .footer {{ 
                background: #28a745;
                color: white;
                padding: 25px 30px; 
                text-align: center;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <div class="logo-container">
                    <img src="data:image/png;base64,{logo_base64}" alt="HelpOP Logo" class="logo-image">
                </div>
                <h1>🎉 Conta Aprovada!</h1>
                <p>Bem-vindo à família HelpOP</p>
            </div>
            
            <div class="content">
                <div class="success-icon">🚀</div>
                
                <div class="welcome-text">
                    Parabéns, <strong>{usuario.first_name or usuario.username}</strong>!
                </div>
                
                <div class="description">
                    Sua conta de <strong>{tipo_usuario}</strong> foi aprovada com sucesso! 
                    Agora você pode acessar todas as funcionalidades da plataforma HelpOP.
                </div>
                
                <div class="button-container">
                    <a href="http://dev.helpop.com.br/login/" class="login-button">
                        Fazer Login Agora
                    </a>
                </div>
                
                <div class="benefits">
                    <h3>O que você pode fazer agora:</h3>
                    <ul>
                        <li>Acessar seu dashboard personalizado</li>
                        <li>Gerenciar serviços e clientes</li>
                        <li>Utilizar sistema de checklists</li>
                        <li>Receber notificações importantes</li>
                        <li>Conectar-se com outros profissionais</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; color: #666;">
                    <p>Atenciosamente,<br>
                    <strong>Equipe HelpOP</strong></p>
                </div>
            </div>
            
            <div class="footer">
                <p><strong>HelpOP</strong> - Sua plataforma de serviços automotivos</p>
                <p style="font-size: 12px; opacity: 0.8; margin-top: 10px;">
                    © 2024 HelpOP. Todos os direitos reservados.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Mensagem de texto simples
    mensagem_texto = f"""
    🎉 CONTA APROVADA! 🎉
    
    Olá {usuario.first_name or usuario.username}!
    
    Parabéns! Sua conta de {tipo_usuario} foi aprovada com sucesso!
    
    Agora você pode acessar todas as funcionalidades da plataforma HelpOP:
    
    ✓ Dashboard personalizado
    ✓ Gerenciamento de serviços
    ✓ Sistema de checklists
    ✓ Notificações importantes
    ✓ Conexão com outros profissionais
    
    Acesse: http://dev.helpop.com.br/login/
    
    Bem-vindo à família HelpOP!
    
    Atenciosamente,
    Equipe HelpOP
    """
    
    try:
        send_mail(
            subject=assunto,
            message=mensagem_texto,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[usuario.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Erro ao enviar email de aprovação: {e}")
        return False

def enviar_email_rejeicao(usuario, motivo="Não especificado"):
    """
    Envia email de rejeição para profissional/oficina
    """
    # Carregar logo
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'ChatGPT Image 28_07_2025, 23_09_31.png')
    with open(logo_path, 'rb') as f:
        logo_data = f.read()
    logo_base64 = base64.b64encode(logo_data).decode('utf-8')
    
    tipo_usuario = "Profissional" if usuario.is_profissional else "Oficina"
    assunto = f'Solicitação de Cadastro - HelpOP {tipo_usuario}'
    
    # Template HTML para rejeição
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Solicitação de Cadastro - HelpOP</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                line-height: 1.6; 
                color: #333; 
                background: #f5f5f5;
                padding: 20px;
            }}
            .email-container {{ 
                max-width: 600px; 
                margin: 0 auto; 
                background: white;
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}
            .header {{ 
                background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); 
                color: white; 
                padding: 30px 20px; 
                text-align: center; 
            }}
            .logo-container {{
                display: inline-block;
                width: 80px;
                height: 80px;
                background: #ffd700;
                border-radius: 50%;
                margin-bottom: 15px;
                border: 3px solid white;
                box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
            }}
            .logo-image {{
                width: 100%;
                height: 100%;
                object-fit: contain;
                border-radius: 50%;
            }}
            .header h1 {{
                font-size: 28px;
                margin-bottom: 5px;
                color: white;
                font-weight: bold;
            }}
            .content {{ 
                padding: 40px 30px; 
                background: white;
            }}
            .info-icon {{
                text-align: center;
                font-size: 60px;
                margin-bottom: 20px;
            }}
            .welcome-text {{
                font-size: 18px;
                color: #1a1a1a;
                margin-bottom: 20px;
                font-weight: 500;
                text-align: center;
            }}
            .description {{
                color: #666;
                margin-bottom: 30px;
                font-size: 16px;
                text-align: center;
            }}
            .reason-box {{
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                color: #856404;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
            }}
            .reason-box h3 {{
                color: #856404;
                margin-bottom: 10px;
            }}
            .next-steps {{
                background: #d1ecf1;
                border-left: 4px solid #17a2b8;
                padding: 20px;
                margin: 20px 0;
                border-radius: 0 8px 8px 0;
            }}
            .next-steps h3 {{
                color: #17a2b8;
                margin-bottom: 10px;
            }}
            .contact-info {{
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
                text-align: center;
            }}
            .footer {{ 
                background: #6c757d;
                color: white;
                padding: 25px 30px; 
                text-align: center;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <div class="logo-container">
                    <img src="data:image/png;base64,{logo_base64}" alt="HelpOP Logo" class="logo-image">
                </div>
                <h1>Solicitação de Cadastro</h1>
                <p>HelpOP - Plataforma de Serviços Automotivos</p>
            </div>
            
            <div class="content">
                <div class="info-icon">📋</div>
                
                <div class="welcome-text">
                    Olá, <strong>{usuario.first_name or usuario.username}</strong>
                </div>
                
                <div class="description">
                    Agradecemos seu interesse em fazer parte da plataforma HelpOP como <strong>{tipo_usuario}</strong>.
                </div>
                
                <div class="reason-box">
                    <h3>📋 Status da Solicitação</h3>
                    <p>Após análise dos dados fornecidos, informamos que sua solicitação de cadastro não pôde ser aprovada neste momento.</p>
                    <br>
                    <p><strong>Motivo:</strong> {motivo}</p>
                </div>
                
                <div class="next-steps">
                    <h3>💡 Próximos Passos</h3>
                    <p>Caso deseje, você pode:</p>
                    <ul style="margin-top: 10px; padding-left: 20px;">
                        <li>Entrar em contato conosco para esclarecimentos</li>
                        <li>Reenviar sua solicitação com as informações corretas</li>
                        <li>Solicitar uma revisão da decisão</li>
                    </ul>
                </div>
                
                <div class="contact-info">
                    <h3>📞 Contato</h3>
                    <p>Entre em contato conosco:</p>
                    <p><strong>Email:</strong> contato@helpop.com.br</p>
                    <p><strong>Suporte:</strong> suporte@helpop.com.br</p>
                </div>
                
                <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; color: #666;">
                    <p>Atenciosamente,<br>
                    <strong>Equipe HelpOP</strong></p>
                </div>
            </div>
            
            <div class="footer">
                <p><strong>HelpOP</strong> - Sua plataforma de serviços automotivos</p>
                <p style="font-size: 12px; opacity: 0.8; margin-top: 10px;">
                    © 2024 HelpOP. Todos os direitos reservados.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Mensagem de texto simples
    mensagem_texto = f"""
    SOLICITAÇÃO DE CADASTRO - HELPOP
    
    Olá {usuario.first_name or usuario.username}!
    
    Agradecemos seu interesse em fazer parte da plataforma HelpOP como {tipo_usuario}.
    
    Após análise dos dados fornecidos, informamos que sua solicitação de cadastro não pôde ser aprovada neste momento.
    
    Motivo: {motivo}
    
    PRÓXIMOS PASSOS:
    • Entre em contato conosco para esclarecimentos
    • Reenvie sua solicitação com as informações corretas
    • Solicite uma revisão da decisão
    
    CONTATO:
    Email: contato@helpop.com.br
    Suporte: suporte@helpop.com.br
    
    Atenciosamente,
    Equipe HelpOP
    """
    
    try:
        send_mail(
            subject=assunto,
            message=mensagem_texto,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[usuario.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Erro ao enviar email de rejeição: {e}")
        return False 