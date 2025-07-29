# Documentação Swagger - HelpOP API

## **🎯 Visão Geral**

A documentação Swagger/OpenAPI foi configurada para fornecer uma interface interativa completa da API HelpOP.

## **📋 URLs de Documentação**

### **Swagger UI:**
- **URL:** `http://localhost:8000/swagger/`
- **Descrição:** Interface interativa para testar a API
- **Recursos:** Teste de endpoints, visualização de schemas, autenticação

### **ReDoc:**
- **URL:** `http://localhost:8000/redoc/`
- **Descrição:** Documentação em formato mais limpo e organizado
- **Recursos:** Visualização hierárquica dos endpoints

### **JSON Schema:**
- **URL:** `http://localhost:8000/swagger.json`
- **Descrição:** Schema OpenAPI em formato JSON
- **Uso:** Para integração com ferramentas externas

## **🔐 Autenticação no Swagger**

### **Para Testar Endpoints Protegidos:**

1. **Faça login** via `/admin/` ou `/login/`
2. **Acesse o Swagger** em `/swagger/`
3. **Clique em "Authorize"** no topo da página
4. **Use cookies de sessão** ou configure autenticação por token

### **Exemplo de Cookie de Sessão:**
```
sessionid=your_session_id_here
```

## **📋 Endpoints Documentados**

### **👥 Usuários**
- `GET /api/usuarios/` - Lista usuários (apenas admin)
- `GET /api/usuarios/{id}/` - Detalhes do usuário
- `GET /api/usuarios/me/` - Dados do usuário logado
- `POST /api/usuarios/` - Criar usuário
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

## **🔐 Permissões Documentadas**

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

## **📊 Exemplos de Uso no Swagger**

### **1. Criar um Veículo:**
```json
{
  "marca": "Toyota",
  "modelo": "Corolla",
  "ano": 2020,
  "placa": "ABC1234",
  "km_atual": 50000
}
```

### **2. Executar um Checklist:**
```json
{
  "checklist": 1,
  "veiculo": 1,
  "observacoes": "Verificação completa realizada"
}
```

### **3. Atualizar Item de Checklist:**
```json
{
  "checked": true,
  "resultado": "aprovado",
  "observacoes": "Item verificado e aprovado"
}
```

## **🎯 Como Usar o Swagger**

### **1. Acesse a Documentação:**
- Vá para `http://localhost:8000/swagger/`

### **2. Faça Login:**
- Clique em "Authorize" no topo
- Configure a autenticação com cookies de sessão

### **3. Teste os Endpoints:**
- Clique em qualquer endpoint
- Clique em "Try it out"
- Preencha os parâmetros necessários
- Clique em "Execute"

### **4. Visualize as Respostas:**
- Veja o código de status
- Analise o corpo da resposta
- Verifique os headers

## **🚀 Benefícios do Swagger**

### **Para Desenvolvedores:**
- ✅ **Documentação interativa** e sempre atualizada
- ✅ **Teste de endpoints** diretamente na interface
- ✅ **Visualização de schemas** e modelos de dados
- ✅ **Exemplos de requisições** e respostas

### **Para Mobile Developers:**
- ✅ **Geração automática** de código cliente
- ✅ **Documentação clara** de todos os endpoints
- ✅ **Teste de integração** antes da implementação
- ✅ **Validação de dados** e tipos

### **Para QA/Testers:**
- ✅ **Interface para testes** da API
- ✅ **Validação de respostas** e códigos de status
- ✅ **Teste de diferentes cenários** de uso
- ✅ **Documentação de casos de teste**

## **🎉 Swagger Configurado com Sucesso!**

A documentação Swagger está **100% funcional** e pronta para uso! ✨📚 