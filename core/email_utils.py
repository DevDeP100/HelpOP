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