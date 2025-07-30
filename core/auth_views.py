from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Usuario

@swagger_auto_schema(
    method='post',
    operation_description="Login de usuário via API usando username e password",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Nome de usuário ou email'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Senha do usuário'),
        },
        required=['username', 'password']
    ),
    responses={
        200: openapi.Response(
            description="Login bem-sucedido",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'token': openapi.Schema(type=openapi.TYPE_STRING, description='Token de autenticação'),
                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID do usuário'),
                    'username': openapi.Schema(type=openapi.TYPE_STRING, description='Nome de usuário'),
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email do usuário'),
                    'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='Primeiro nome'),
                    'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Sobrenome'),
                    'is_staff': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='É administrador'),
                    'is_profissional': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='É profissional'),
                    'is_oficina': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='É oficina'),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description='Mensagem de sucesso'),
                }
            )
        ),
        400: 'Credenciais inválidas ou campos obrigatórios',
        401: 'Usuário inativo ou não autorizado',
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    """
    Login de usuário via API usando username/email e password.
    
    Retorna um token de autenticação que deve ser usado nos headers
    das requisições subsequentes como: Authorization: Token <token>
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Username e password são obrigatórios',
            'detail': 'Forneça username/email e password no corpo da requisição'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Tentar autenticar com username ou email
    user = None
    
    # Primeiro tenta com username
    user = authenticate(username=username, password=password)
    
    # Se não encontrou, tenta com email
    if not user:
        try:
            user_obj = Usuario.objects.get(email=username)
            user = authenticate(username=user_obj.username, password=password)
        except Usuario.DoesNotExist:
            pass
    
    if user:
        if user.is_active:
            # Criar ou obter token
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name or '',
                'last_name': user.last_name or '',
                'is_staff': user.is_staff,
                'is_profissional': user.is_profissional,
                'is_oficina': user.is_oficina,
                'message': 'Login realizado com sucesso!',
                'detail': 'Use o token no header Authorization: Token <token>'
            })
        else:
            return Response({
                'error': 'Usuário inativo',
                'detail': 'Entre em contato com o administrador para ativar sua conta'
            }, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({
            'error': 'Credenciais inválidas',
            'detail': 'Verifique seu username/email e senha'
        }, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    operation_description="Logout de usuário via API",
    responses={
        200: 'Logout realizado com sucesso',
        401: 'Não autorizado',
    }
)
@api_view(['POST'])
def api_logout(request):
    """
    Logout de usuário via API.
    
    Remove o token de autenticação do usuário.
    """
    try:
        # Deletar o token atual
        request.user.auth_token.delete()
        return Response({
            'message': 'Logout realizado com sucesso!',
            'detail': 'Token removido com sucesso'
        })
    except Exception as e:
        return Response({
            'error': 'Erro ao fazer logout',
            'detail': str(e)
        }, status=status.HTTP_400_BAD_REQUEST) 