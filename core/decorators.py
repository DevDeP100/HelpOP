from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from functools import wraps

def profissional_required(view_func):
    """
    Decorator que verifica se o usuário é profissional ou oficina
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if not (request.user.is_profissional or request.user.is_oficina):
            messages.error(request, 'Acesso restrito apenas para profissionais e oficinas.')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def oficina_required(view_func):
    """
    Decorator que verifica se o usuário é uma oficina
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if not request.user.is_oficina:
            messages.error(request, 'Acesso restrito apenas para oficinas.')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view 