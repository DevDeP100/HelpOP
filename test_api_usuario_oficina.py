#!/usr/bin/env python3
"""
Script de teste para a API do modelo usuarioOficina
"""

import requests
import json

# Configurações da API
BASE_URL = "http://localhost:8001/api"
LOGIN_URL = f"{BASE_URL}/login/"
USUARIOS_OFICINA_URL = f"{BASE_URL}/usuarios-oficina/"

def test_api_usuario_oficina():
    """Testa a API do usuarioOficina"""
    
    print("🧪 TESTANDO API USUARIO OFICINA")
    print("=" * 50)
    
    # 1. Fazer login para obter token
    print("\n1️⃣ Fazendo login...")
    login_data = {
        "username": "api_test",
        "password": "api123"
    }
    
    try:
        response = requests.post(LOGIN_URL, data=login_data)
        if response.status_code == 200:
            print("✅ Login realizado com sucesso!")
            print(f"   - Status: {response.status_code}")
            
            # Extrair token da resposta
            response_data = response.json()
            if 'token' in response_data:
                token = response_data['token']
                print(f"   - Token obtido: {token[:20]}...")
            else:
                print("❌ Token não encontrado na resposta")
                print(f"   - Resposta: {response_data}")
                return False
        else:
            print(f"❌ Falha no login: {response.status_code}")
            print(f"   - Resposta: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão. Verifique se o servidor está rodando em http://localhost:8001")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False
    
    # 2. Testar endpoint de listagem
    print("\n2️⃣ Testando endpoint de listagem...")
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(USUARIOS_OFICINA_URL, headers=headers)
        print(f"   - Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   - Resposta completa: {data}")
            
            # Verificar se é uma lista ou objeto com paginação
            if isinstance(data, list):
                print(f"   - Total de registros: {len(data)}")
                
                if data:
                    print("   - Primeiro registro:")
                    primeiro = data[0]
                    print(f"     * ID: {primeiro.get('id')}")
                    print(f"     * Usuário: {primeiro.get('usuario_nome', 'N/A')}")
                    print(f"     * Oficina: {primeiro.get('oficina_nome', 'N/A')}")
                    print(f"     * Ativo: {primeiro.get('ativo')}")
                else:
                    print("   - Nenhum registro encontrado")
            elif isinstance(data, dict) and 'results' in data:
                results = data['results']
                print(f"   - Total de registros: {len(results)}")
                
                if results:
                    print("   - Primeiro registro:")
                    primeiro = results[0]
                    print(f"     * ID: {primeiro.get('id')}")
                    print(f"     * Usuário: {primeiro.get('usuario_nome', 'N/A')}")
                    print(f"     * Oficina: {primeiro.get('oficina_nome', 'N/A')}")
                    print(f"     * Ativo: {primeiro.get('ativo')}")
                else:
                    print("   - Nenhum registro encontrado")
            else:
                print(f"   - Formato de resposta inesperado: {type(data)}")
                
        else:
            print(f"   - Erro: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro ao testar listagem: {e}")
        import traceback
        traceback.print_exc()
    
    # 3. Testar endpoint de relacionamentos ativos
    print("\n3️⃣ Testando endpoint de relacionamentos ativos...")
    try:
        response = requests.get(f"{USUARIOS_OFICINA_URL}ativos/", headers=headers)
        print(f"   - Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   - Total de relacionamentos ativos: {len(data)}")
        else:
            print(f"   - Erro: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro ao testar ativos: {e}")
    
    # 4. Testar endpoint por oficina (se houver oficinas)
    print("\n4️⃣ Testando endpoint por oficina...")
    try:
        # Primeiro, buscar oficinas disponíveis
        oficinas_response = requests.get(f"{BASE_URL}/oficinas/", headers=headers)
        if oficinas_response.status_code == 200:
            oficinas_data = oficinas_response.json()
            print(f"   - Resposta oficinas: {oficinas_data}")
            
            # Verificar se é uma lista ou objeto com paginação
            if isinstance(oficinas_data, list):
                oficinas = oficinas_data
            elif isinstance(oficinas_data, dict) and 'results' in oficinas_data:
                oficinas = oficinas_data['results']
            else:
                oficinas = []
            
            if oficinas:
                primeira_oficina = oficinas[0]
                oficina_id = primeira_oficina['id']
                print(f"   - Testando com oficina ID: {oficina_id}")
                
                response = requests.get(f"{USUARIOS_OFICINA_URL}por_oficina/?oficina_id={oficina_id}", headers=headers)
                print(f"   - Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"   - Total de usuários na oficina: {len(data)}")
                else:
                    print(f"   - Erro: {response.text}")
            else:
                print("   - Nenhuma oficina encontrada para teste")
        else:
            print(f"   - Erro ao buscar oficinas: {oficinas_response.text}")
            
    except Exception as e:
        print(f"❌ Erro ao testar por oficina: {e}")
        import traceback
        traceback.print_exc()
    
    # 5. Testar criação de novo relacionamento (se possível)
    print("\n5️⃣ Testando criação de relacionamento...")
    try:
        # Buscar usuário e oficina disponíveis
        usuarios_response = requests.get(f"{BASE_URL}/usuarios/", headers=headers)
        oficinas_response = requests.get(f"{BASE_URL}/oficinas/", headers=headers)
        
        if usuarios_response.status_code == 200 and oficinas_response.status_code == 200:
            usuarios_data = usuarios_response.json()
            oficinas_data = oficinas_response.json()
            
            # Verificar se são listas ou objetos com paginação
            if isinstance(usuarios_data, list):
                usuarios = usuarios_data
            elif isinstance(usuarios_data, dict) and 'results' in usuarios_data:
                usuarios = usuarios_data['results']
            else:
                usuarios = []
                
            if isinstance(oficinas_data, list):
                oficinas = oficinas_data
            elif isinstance(oficinas_data, dict) and 'results' in oficinas_data:
                oficinas = oficinas_data['results']
            else:
                oficinas = []
            
            if usuarios and oficinas:
                usuario_id = usuarios[0]['id']
                oficina_id = oficinas[0]['id']
                
                novo_relacionamento = {
                    "usuario": usuario_id,
                    "oficina": oficina_id,
                    "ativo": True,
                    "created_by": usuario_id,
                    "updated_by": usuario_id
                }
                
                response = requests.post(USUARIOS_OFICINA_URL, json=novo_relacionamento, headers=headers)
                print(f"   - Status: {response.status_code}")
                
                if response.status_code == 201:
                    print("✅ Relacionamento criado com sucesso!")
                    data = response.json()
                    print(f"   - ID criado: {data.get('id')}")
                    
                    # Limpar - deletar o relacionamento criado
                    delete_response = requests.delete(f"{USUARIOS_OFICINA_URL}{data.get('id')}/", headers=headers)
                    if delete_response.status_code == 204:
                        print("   - Relacionamento de teste removido")
                    else:
                        print(f"   - Erro ao remover: {delete_response.status_code}")
                        
                else:
                    print(f"   - Erro: {response.text}")
            else:
                print("   - Usuários ou oficinas não encontrados para teste")
        else:
            print(f"   - Erro ao buscar dados para teste")
            
    except Exception as e:
        print(f"❌ Erro ao testar criação: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 TESTE CONCLUÍDO!")
    
    return True

if __name__ == "__main__":
    test_api_usuario_oficina()
