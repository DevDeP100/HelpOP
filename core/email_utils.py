from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import CodigoVerificacao

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
    
    # Template HTML para o email
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); 
                      color: #ffd700; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .codigo {{ background: #ffd700; color: #1a1a1a; padding: 15px; 
                      font-size: 24px; font-weight: bold; text-align: center; 
                      border-radius: 8px; margin: 20px 0; letter-spacing: 3px; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            .btn {{ display: inline-block; background: #ffd700; color: #1a1a1a; 
                   padding: 12px 24px; text-decoration: none; border-radius: 5px; 
                   font-weight: bold; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚗 HelpOP</h1>
                <p>Sua plataforma de serviços automotivos</p>
            </div>
            <div class="content">
                <h2>Olá {usuario.first_name or usuario.username}!</h2>
                <p>Bem-vindo ao HelpOP! Para completar seu cadastro e começar a usar nossa plataforma, 
                use o código de verificação abaixo:</p>
                
                <div class="codigo">{codigo}</div>
                
                <p><strong>Este código expira em 24 horas.</strong></p>
                
                <p>Se você não solicitou este cadastro, ignore este email.</p>
                
                <p>Atenciosamente,<br>
                <strong>Equipe HelpOP</strong></p>
            </div>
            <div class="footer">
                <p>© 2024 HelpOP. Todos os direitos reservados.</p>
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