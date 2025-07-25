# Sistema de Aprovação - HelpOP
## Visão Geral

O sistema de aprovação foi implementado para controlar o acesso de profissionais e oficinas à plataforma HelpOP. Após o cadastro e verificação de email, profissionais e oficinas ficam com status "pendente" até serem aprovados por um administrador.

## Funcionalidades Implementadas

### 1. Modelo de Dados
- **Campo `aprovado_pendente`** no modelo `Usuario`
- Controla se o usuário está aguardando aprovação do administrador
- Padrão: `False` (aprovado automaticamente para usuários comuns)

### 2. Fluxo de Cadastro
1. **Usuário comum**: Cadastro → Verificação de email → Acesso liberado
2. **Profissional/Oficina**: Cadastro → Verificação de email → **Aguardando aprovação** → Aprovação do admin → Acesso liberado

### 3. Views de Administração

#### `admin_dashboard`
- Dashboard administrativo com estatísticas
- Acesso restrito a usuários `is_staff=True`
- Mostra:
  - Total de usuários
  - Usuários pendentes de aprovação
  - Profissionais aprovados
  - Oficinas aprovadas
  - Lista de usuários pendentes recentes

#### `admin_aprovar_usuarios`
- Interface para aprovar/rejeitar usuários pendentes
- Ações disponíveis:
  - **Aprovar**: Remove `aprovado_pendente=True` e aprova o perfil profissional
  - **Rejeitar**: Remove o usuário do sistema

### 4. Controle de Acesso

#### Login
- Verifica se o email foi confirmado
- **Para profissionais/oficinas**: Verifica se está aprovado
- Bloqueia login se `aprovado_pendente=True`

#### Templates
- Mensagens informativas durante o processo
- Alertas sobre aprovação pendente
- Interface administrativa integrada

### 5. URLs Implementadas
```
/admin-dashboard/          # Dashboard administrativo
/admin/aprovar-usuarios/  # Interface de aprovação
```

## Como Usar

### Para Administradores

1. **Acessar Dashboard Admin**:
   - Login como usuário com `is_staff=True`
   - Menu: "Dashboard Admin" no dropdown do usuário

2. **Aprovar Usuários**:
   - Acessar "Aprovar Usuários"
   - Ver lista de usuários pendentes
   - Clicar em "Aprovar" ou "Rejeitar"

3. **Monitoramento**:
   - Dashboard mostra estatísticas em tempo real
   - Lista de usuários pendentes recentes

### Para Profissionais/Oficinas

1. **Cadastro**:
   - Marcar checkbox "Sou um profissional" ou "Sou uma oficina"
   - Preencher dados normalmente

2. **Verificação**:
   - Confirmar email
   - Receber mensagem sobre aprovação pendente

3. **Aguardar Aprovação**:
   - Não conseguem fazer login até serem aprovados
   - Receberão notificação quando aprovados

## Configuração

### Criar Superusuário
```bash
python manage.py createsuperuser
```

### Verificar Migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

## Segurança

- Acesso administrativo restrito a `is_staff=True`
- Verificação de permissões em todas as views administrativas
- Confirmação antes de rejeitar usuários
- Logs de ações administrativas (futuro)

## Próximas Melhorias

1. **Notificações por Email**:
   - Email automático quando usuário é aprovado
   - Email de rejeição com motivo

2. **Logs de Auditoria**:
   - Registrar todas as ações administrativas
   - Histórico de aprovações/rejeições

3. **Filtros Avançados**:
   - Buscar usuários por tipo, data, etc.
   - Ordenação e paginação

4. **Perfil Detalhado**:
   - Ver mais informações do usuário antes de aprovar
   - Documentos/credenciais (futuro) 