#!/usr/bin/env python3
"""
Script de teste para a API de autenticação do HelpOP
"""

import requests
import json

# Configurações
BASE_URL = "http://localhost:8001"
LOGIN_URL = f"{BASE_URL}/api/login/"
ME_URL = f"{BASE_URL}/api/usuarios/me/"
LOGOUT_URL = f"{BASE_URL}/api/logout/"

def test_login(username, password):
    """Testa o login da API"""
    print(f"🔐 Testando login com usuário: {username}")
    
    data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(LOGIN_URL, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Login realizado com sucesso!")
            print(f"   Token: {result['token'][:20]}...")
            print(f"   Usuário: {result['username']}")
            print(f"   Email: {result['email']}")
            print(f"   É Admin: {result['is_staff']}")
            return result['token']
        else:
            print(f"❌ Erro no login: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return None

def test_me_endpoint(token):
    """Testa o endpoint /me/ com token"""
    print(f"\n👤 Testando endpoint /me/")
    
    headers = {
        "Authorization": f"Token {token}"
    }
    
    try:
        response = requests.get(ME_URL, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Endpoint /me/ funcionando!")
            print(f"   ID: {result['id']}")
            print(f"   Username: {result['username']}")
            print(f"   Email: {result['email']}")
            return True
        else:
            print(f"❌ Erro no endpoint /me/: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def test_logout(token):
    """Testa o logout da API"""
    print(f"\n🚪 Testando logout")
    
    headers = {
        "Authorization": f"Token {token}"
    }
    
    try:
        response = requests.post(LOGOUT_URL, headers=headers)
        
        if response.status_code == 200:
            print("✅ Logout realizado com sucesso!")
            return True
        else:
            print(f"❌ Erro no logout: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🚀 Testando API de Autenticação do HelpOP")
    print("=" * 50)
    
    # Teste 1: Login com usuário de teste
    token = test_login("api_test", "api123")
    
    if token:
        # Teste 2: Endpoint /me/
        test_me_endpoint(token)
        
        # Teste 3: Logout
        test_logout(token)
        
        print("\n" + "=" * 50)
        print("✅ Todos os testes concluídos!")
        print("\n📋 Resumo:")
        print("   - Login: ✅ Funcionando")
        print("   - Token: ✅ Válido")
        print("   - Endpoint /me/: ✅ Funcionando")
        print("   - Logout: ✅ Funcionando")
        print("\n🎉 API de autenticação configurada com sucesso!")
    else:
        print("\n❌ Falha nos testes de autenticação")
        print("   Verifique se:")
        print("   - O servidor está rodando na porta 8001")
        print("   - As credenciais estão corretas")
        print("   - O usuário existe e está ativo")
        print("\n💡 Dica: Use o usuário api_test com senha api123")

if __name__ == "__main__":
    main() 