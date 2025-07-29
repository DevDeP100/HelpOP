# Sistema de Checklist - HelpOP

## 📋 Models Criados

### 1. **TipoVeiculo**
- **Propósito:** Tipos de veículos (carro, moto, caminhão, etc.)
- **Campos:**
  - `nome` (CharField): Nome do tipo de veículo
  - `descricao` (TextField): Descrição detalhada
  - `ativo` (BooleanField): Se está ativo
  - `data_criacao` (DateTimeField): Data de criação

### 2. **CategoriaChecklist**
- **Propósito:** Categorias do checklist (motor, freios, elétrica, etc.)
- **Campos:**
  - `nome` (CharField): Nome da categoria
  - `descricao` (TextField): Descrição da categoria
  - `ordem` (PositiveIntegerField): Ordem de exibição
  - `ativo` (BooleanField): Se está ativa
  - `data_criacao` (DateTimeField): Data de criação

### 3. **ItemChecklist**
- **Propósito:** Itens individuais do checklist
- **Campos:**
  - `categoria` (ForeignKey): Categoria do item
  - `nome` (CharField): Nome do item
  - `descricao` (TextField): Descrição detalhada
  - `tipo_verificacao` (CharField): Tipo de verificação (visual, teste, medição, inspeção)
  - `critico` (BooleanField): Se é item crítico para segurança
  - `ordem` (PositiveIntegerField): Ordem dentro da categoria
  - `ativo` (BooleanField): Se está ativo
  - `data_criacao` (DateTimeField): Data de criação

### 4. **Checklist**
- **Propósito:** Checklist personalizado de uma oficina para um tipo de veículo
- **Campos:**
  - `oficina` (ForeignKey): Oficina proprietária
  - `tipo_veiculo` (ForeignKey): Tipo de veículo
  - `nome` (CharField): Nome do checklist
  - `descricao` (TextField): Descrição do checklist
  - `ativo` (BooleanField): Se está ativo
  - `data_criacao` (DateTimeField): Data de criação
  - `data_atualizacao` (DateTimeField): Data da última atualização

### 5. **ItemChecklistPersonalizado**
- **Propósito:** Itens personalizados do checklist da oficina
- **Campos:**
  - `checklist` (ForeignKey): Checklist ao qual pertence
  - `item_padrao` (ForeignKey): Item padrão do sistema (opcional)
  - `nome` (CharField): Nome do item
  - `descricao` (TextField): Descrição do item
  - `categoria` (ForeignKey): Categoria do item
  - `tipo_verificacao` (CharField): Tipo de verificação
  - `critico` (BooleanField): Se é item crítico
  - `obrigatorio` (BooleanField): Se é item obrigatório
  - `ordem` (PositiveIntegerField): Ordem de exibição
  - `ativo` (BooleanField): Se está ativo
  - `data_criacao` (DateTimeField): Data de criação

## 🎯 Funcionalidades

### **Relacionamentos:**
- **Uma oficina** pode ter **múltiplos checklists** para **diferentes tipos de veículos**
- **Cada checklist** pode ter **itens personalizados** baseados nos **itens padrão** do sistema
- **Itens críticos** são destacados para **segurança**
- **Ordem de exibição** controlada para **melhor organização**

### **Tipos de Verificação:**
1. **Visual:** Verificação visual simples
2. **Teste:** Teste funcional
3. **Medição:** Medição com instrumentos
4. **Inspeção:** Inspeção detalhada

## 📊 Dados Iniciais Criados

### **Tipos de Veículos (6):**
- Carro
- Moto
- Caminhão
- Ônibus
- Van
- Caminhonete

### **Categorias (10):**
1. Motor
2. Sistema de Freios
3. Suspensão
4. Sistema Elétrico
5. Sistema de Arrefecimento
6. Sistema de Combustível
7. Transmissão
8. Pneus e Rodas
9. Iluminação
10. Segurança

### **Itens Padrão (40):**
- **Motor:** 5 itens (nível óleo, filtros, correias, vazamentos)
- **Sistema de Freios:** 5 itens (fluido, pastilhas, discos, cilindros, freio mão)
- **Suspensão:** 4 itens (amortecedores, molas, buchas, bandejas)
- **Sistema Elétrico:** 4 itens (bateria, alternador, motor partida, fusíveis)
- **Sistema de Arrefecimento:** 4 itens (líquido, radiador, mangueiras, bomba água)
- **Sistema de Combustível:** 3 itens (filtro, bomba, bicos injetores)
- **Transmissão:** 3 itens (óleo, embreagem, diferencial)
- **Pneus e Rodas:** 4 itens (pressão, desgaste, alinhamento, balanceamento)
- **Iluminação:** 4 itens (faróis, lanternas, setas, luz freio)
- **Segurança:** 4 itens (cintos, airbags, extintor, triângulo)

## 🔧 Comandos Disponíveis

### **Popular dados iniciais:**
```bash
python manage.py popular_checklist
```

### **Criar migrações:**
```bash
python manage.py makemigrations
```

### **Aplicar migrações:**
```bash
python manage.py migrate
```

## 🎨 Admin Django

Todos os models estão registrados no admin do Django com:
- **List displays** organizados
- **Filtros** por campos relevantes
- **Campos editáveis** em lista
- **Busca** por texto
- **Ordenação** adequada

## 🚀 Próximos Passos

1. **Criar views** para gerenciar checklists
2. **Criar templates** para interface do usuário
3. **Implementar funcionalidades** de criação/edição
4. **Adicionar validações** específicas
5. **Criar relatórios** de checklist 