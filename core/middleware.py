from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class EmailVerificationMiddleware:
    """
    Middleware para verificar se o usuário logado tem email verificado.
    Se não tiver, redireciona para a página de verificação.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs que não precisam de verificação de email
        self.exempt_urls = [
            '/login/',
            '/logout/',
            '/cadastro/',
            '/verificar-email/',
            '/reenviar-codigo/',
            '/admin/',
            '/static/',
            '/media/',
            '/api/',
            '/swagger/',
            '/redoc/',
            '/swagger.json',
        ]
        
        # URLs que sempre permitem acesso (mesmo sem email verificado)
        self.always_allowed = [
            '/',
            '/home/',
        ]
    
    def __call__(self, request):
        # Verificar se o usuário está logado
        if request.user.is_authenticated:
            # Verificar se é um usuário normal (não staff/admin)
            if not request.user.is_staff:
                # Verificar se o email não foi verificado
                if not request.user.email_verificado:
                    # Verificar se a URL atual não está na lista de exceções
                    current_path = request.path
                    
                    # Permitir sempre acesso às URLs sempre permitidas
                    if any(current_path.startswith(url) for url in self.always_allowed):
                        pass
                    # Verificar se a URL atual não está na lista de exceções
                    elif not any(current_path.startswith(url) for url in self.exempt_urls):
                        # Se não estiver na lista de exceções, redirecionar para verificação
                        return redirect('verificar_email', user_id=request.user.id)
        
        response = self.get_response(request)
        return response
