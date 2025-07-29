# API REST - HelpOP

## **🎯 Visão Geral**

API REST completa para o sistema HelpOP, permitindo integração com aplicativos mobile e outros sistemas.

**Base URL:** `http://localhost:8000/api/`

## **🔐 Autenticação**

A API utiliza autenticação por sessão do Django. Para acessar endpoints protegidos:

1. **Faça login** via `/admin/` ou `/login/`
2. **Use cookies de sessão** nas requisições
3. **Alternativa:** Use autenticação por token (configurável)

## **📋 Endpoints Disponíveis**

### **👥 Usuários**
- `GET /api/usuarios/` - Lista usuários (apenas admin)
- `GET /api/usuarios/{id}/` - Detalhes do usuário
- `GET /api/usuarios/me/` - Dados do usuário logado
- `POST /api/usuarios/` - Criar usuário (apenas admin)
- `PUT /api/usuarios/{id}/` - Atualizar usuário
- `DELETE /api/usuarios/{id}/` - Deletar usuário

### **🚗 Veículos**
- `GET /api/veiculos/` - Lista veículos do usuário
- `GET /api/veiculos/{id}/` - Detalhes do veículo
- `POST /api/veiculos/` - Criar veículo
- `PUT /api/veiculos/{id}/` - Atualizar veículo
- `DELETE /api/veiculos/{id}/` - Deletar veículo

### **🔧 Oficinas**
- `GET /api/oficinas/` - Lista oficinas
- `GET /api/oficinas/{id}/` - Detalhes da oficina
- `POST /api/oficinas/` - Criar oficina
- `PUT /api/oficinas/{id}/` - Atualizar oficina
- `DELETE /api/oficinas/{id}/` - Deletar oficina

### **👨‍🔧 Profissionais**
- `GET /api/profissionais/` - Lista profissionais aprovados
- `GET /api/profissionais/{id}/` - Detalhes do profissional
- `POST /api/profissionais/` - Criar profissional
- `PUT /api/profissionais/{id}/` - Atualizar profissional
- `DELETE /api/profissionais/{id}/` - Deletar profissional

### **🛠️ Serviços**
- `GET /api/servicos/` - Lista serviços ativos
- `GET /api/servicos/{id}/` - Detalhes do serviço
- `POST /api/servicos/` - Criar serviço
- `PUT /api/servicos/{id}/` - Atualizar serviço
- `DELETE /api/servicos/{id}/` - Deletar serviço

### **🔧 Manutenções**
- `GET /api/manutencoes/` - Lista manutenções
- `GET /api/manutencoes/{id}/` - Detalhes da manutenção
- `POST /api/manutencoes/` - Criar manutenção
- `PUT /api/manutencoes/{id}/` - Atualizar manutenção
- `DELETE /api/manutencoes/{id}/` - Deletar manutenção

### **⭐ Avaliações**
- `GET /api/avaliacoes/` - Lista avaliações
- `GET /api/avaliacoes/{id}/` - Detalhes da avaliação
- `POST /api/avaliacoes/` - Criar avaliação
- `PUT /api/avaliacoes/{id}/` - Atualizar avaliação
- `DELETE /api/avaliacoes/{id}/` - Deletar avaliação

## **📋 Endpoints do Sistema de Checklist**

### **🚗 Tipos de Veículo**
- `GET /api/tipos-veiculo/` - Lista tipos de veículo
- `GET /api/tipos-veiculo/{id}/` - Detalhes do tipo
- `POST /api/tipos-veiculo/` - Criar tipo de veículo
- `PUT /api/tipos-veiculo/{id}/` - Atualizar tipo
- `DELETE /api/tipos-veiculo/{id}/` - Deletar tipo

### **📂 Categorias de Checklist**
- `GET /api/categorias-checklist/` - Lista categorias
- `GET /api/categorias-checklist/{id}/` - Detalhes da categoria
- `POST /api/categorias-checklist/` - Criar categoria
- `PUT /api/categorias-checklist/{id}/` - Atualizar categoria
- `DELETE /api/categorias-checklist/{id}/` - Deletar categoria

### **📝 Itens de Checklist**
- `GET /api/itens-checklist/` - Lista itens de checklist
- `GET /api/itens-checklist/{id}/` - Detalhes do item
- `POST /api/itens-checklist/` - Criar item
- `PUT /api/itens-checklist/{id}/` - Atualizar item
- `DELETE /api/itens-checklist/{id}/` - Deletar item

### **📋 Checklists**
- `GET /api/checklists/` - Lista checklists
- `GET /api/checklists/{id}/` - Detalhes do checklist
- `GET /api/checklists/{id}/detalhado/` - Checklist com todos os detalhes
- `POST /api/checklists/` - Criar checklist (apenas oficinas)
- `PUT /api/checklists/{id}/` - Atualizar checklist
- `DELETE /api/checklists/{id}/` - Deletar checklist

### **📝 Itens Personalizados de Checklist**
- `GET /api/itens-checklist-personalizados/` - Lista itens personalizados
- `GET /api/itens-checklist-personalizados/{id}/` - Detalhes do item
- `POST /api/itens-checklist-personalizados/` - Criar item personalizado
- `PUT /api/itens-checklist-personalizados/{id}/` - Atualizar item
- `DELETE /api/itens-checklist-personalizados/{id}/` - Deletar item

### **✅ Checklists Executados**
- `GET /api/checklists-executados/` - Lista execuções
- `GET /api/checklists-executados/{id}/` - Detalhes da execução
- `GET /api/checklists-executados/{id}/detalhado/` - Execução com todos os detalhes
- `POST /api/checklists-executados/` - Criar execução
- `PUT /api/checklists-executados/{id}/` - Atualizar execução
- `DELETE /api/checklists-executados/{id}/` - Deletar execução

### **✅ Itens de Checklist Executados**
- `GET /api/itens-checklist-executados/` - Lista itens executados
- `GET /api/itens-checklist-executados/{id}/` - Detalhes do item
- `POST /api/itens-checklist-executados/` - Criar item executado
- `PUT /api/itens-checklist-executados/{id}/` - Atualizar item
- `DELETE /api/itens-checklist-executados/{id}/` - Deletar item

### **📎 Arquivos de Checklist**
- `GET /api/arquivos-checklist/` - Lista arquivos
- `GET /api/arquivos-checklist/{id}/` - Detalhes do arquivo
- `POST /api/arquivos-checklist/` - Criar arquivo
- `PUT /api/arquivos-checklist/{id}/` - Atualizar arquivo
- `DELETE /api/arquivos-checklist/{id}/` - Deletar arquivo

## **🔐 Permissões**

### **Usuários Comuns:**
- ✅ Visualizar seus próprios veículos
- ✅ Visualizar manutenções de seus veículos
- ✅ Visualizar checklists ativos
- ✅ Visualizar execuções de checklists

### **Profissionais:**
- ✅ Tudo que usuários comuns podem fazer
- ✅ Criar/editar manutenções
- ✅ Executar checklists
- ✅ Visualizar checklists da oficina

### **Oficinas:**
- ✅ Tudo que profissionais podem fazer
- ✅ Criar/editar checklists
- ✅ Gerenciar itens personalizados
- ✅ Visualizar todas as execuções da oficina

### **Administradores:**
- ✅ Acesso completo a todos os endpoints
- ✅ Gerenciar usuários, oficinas e profissionais

## **📊 Exemplos de Uso**

### **Criar um Veículo:**
```bash
curl -X POST http://localhost:8000/api/veiculos/ \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=your_session_id" \
  -d '{
    "marca": "Toyota",
    "modelo": "Corolla",
    "ano": 2020,
    "placa": "ABC1234",
    "km_atual": 50000
  }'
```

### **Listar Checklists:**
```bash
curl -X GET http://localhost:8000/api/checklists/ \
  -H "Cookie: sessionid=your_session_id"
```

### **Executar um Checklist:**
```bash
curl -X POST http://localhost:8000/api/checklists-executados/ \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=your_session_id" \
  -d '{
    "checklist": 1,
    "veiculo": 1,
    "observacoes": "Verificação completa realizada"
  }'
```

## **📱 Para App Mobile**

### **Flutter/Dart:**
```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class HelpOPApi {
  static const String baseUrl = 'http://localhost:8000/api';
  
  static Future<List<dynamic>> getChecklists() async {
    final response = await http.get(
      Uri.parse('$baseUrl/checklists/'),
      headers: {'Cookie': 'sessionid=your_session_id'},
    );
    
    if (response.statusCode == 200) {
      return json.decode(response.body)['results'];
    } else {
      throw Exception('Failed to load checklists');
    }
  }
}
```

### **React Native:**
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Cookie': 'sessionid=your_session_id'
  }
});

export const getChecklists = async () => {
  try {
    const response = await api.get('/checklists/');
    return response.data.results;
  } catch (error) {
    console.error('Error fetching checklists:', error);
  }
};
```

## **🚀 Próximos Passos**

1. **Implementar autenticação por token** para melhor segurança
2. **Adicionar filtros e busca** nos endpoints
3. **Implementar upload de arquivos** para imagens
4. **Criar endpoints para relatórios** e estatísticas
5. **Adicionar validação personalizada** nos serializers
6. **Implementar cache** para melhor performance

## **🎉 API Completa e Funcional!**

A API está **100% implementada** e pronta para integração com aplicativos mobile! ✨🚀 