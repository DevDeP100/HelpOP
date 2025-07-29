# Como Usar Imagens da Oficina Jordão no Carrossel

## 🎯 Objetivo
Substituir as imagens atuais do carrossel pelas imagens reais da Oficina Jordão no Papicu, Fortaleza.

## 📋 Passos para Implementar

### 1. Obter as Imagens da Oficina Jordão

**Opções para conseguir as imagens:**

#### A) Se você conhece a oficina:
- Visite o local e tire fotos profissionais
- Peça autorização para usar as imagens
- Foque em: fachada, equipamentos, atendimento, serviços

#### B) Se não conhece:
- Entre em contato com a oficina
- Explique o projeto HelpOP
- Peça permissão para usar imagens
- Ofereça crédito à oficina

#### C) Buscar online:
- Google Maps: "Oficina Jordão Papicu Fortaleza"
- Instagram: "@oficina_jordao"
- Facebook: "Oficina Jordão Fortaleza"
- Google Meu Negócio

### 2. Salvar as Imagens

**Quando tiver as imagens da Oficina Jordão:**

```bash
cd static/images/

# Salvar com nomes específicos
cp imagem_fachada_jordao.jpg oficina1.jpg
cp imagem_equipamentos_jordao.jpg oficina2.jpg
cp imagem_atendimento_jordao.jpg oficina3.jpg
cp imagem_servicos_jordao.jpg oficina4.jpg
```

### 3. Verificar o Carrossel

**O carrossel já está configurado para:**
- ✅ Altura: 400px
- ✅ Largura: 120% do container
- ✅ Rotação automática: 3 segundos
- ✅ Navegação: Setas e indicadores
- ✅ Efeitos: Hover e transições

### 4. Testar as Imagens

```bash
# Verificar se as imagens estão carregando
curl -I http://localhost:8010/static/images/oficina1.jpg
curl -I http://localhost:8010/static/images/oficina2.jpg
curl -I http://localhost:8010/static/images/oficina3.jpg
curl -I http://localhost:8010/static/images/oficina4.jpg
```

### 5. Atualizar Static Files (se necessário)

```bash
python manage.py collectstatic
```

## 🎨 Estrutura do Carrossel

**Arquivo:** `helpOP/templates/home.html`

```html
<div id="oficinasCarousel" class="carousel slide" data-bs-ride="carousel" data-bs-interval="3000" style="width: 120%; margin-left: -10%;">
    <div class="carousel-inner">
        <div class="carousel-item active">
            <img src="{% static 'images/oficina1.jpg' %}" alt="Oficina Jordão - Fachada" class="d-block w-100" style="height: 400px; object-fit: cover; border-radius: 15px;">
        </div>
        <div class="carousel-item">
            <img src="{% static 'images/oficina2.jpg' %}" alt="Oficina Jordão - Equipamentos" class="d-block w-100" style="height: 400px; object-fit: cover; border-radius: 15px;">
        </div>
        <div class="carousel-item">
            <img src="{% static 'images/oficina3.jpg' %}" alt="Oficina Jordão - Atendimento" class="d-block w-100" style="height: 400px; object-fit: cover; border-radius: 15px;">
        </div>
        <div class="carousel-item">
            <img src="{% static 'images/oficina4.jpg' %}" alt="Oficina Jordão - Serviços" class="d-block w-100" style="height: 400px; object-fit: cover; border-radius: 15px;">
        </div>
    </div>
    <!-- Controles e indicadores -->
</div>
```

## 📝 Adicionar Créditos

**Quando usar as imagens da Oficina Jordão, adicionar:**

```html
<!-- Adicionar na página ou footer -->
<div class="text-center mt-3">
    <small class="text-muted">
        Imagens: <a href="[LINK_DA_OFICINA_JORDAO]" target="_blank">Oficina Jordão</a> - Papicu, Fortaleza
    </small>
</div>
```

## 🔄 Backup e Restauração

**Backup atual criado:**
- `oficina1_backup.jpg`
- `oficina2_backup.jpg`
- `oficina3_backup.jpg`
- `oficina4_backup.jpg`

**Para restaurar:**
```bash
cp oficina1_backup.jpg oficina1.jpg
cp oficina2_backup.jpg oficina2.jpg
cp oficina3_backup.jpg oficina3.jpg
cp oficina4_backup.jpg oficina4.jpg
```

## ✅ Checklist

- [ ] Obter imagens da Oficina Jordão
- [ ] Pedir autorização para usar
- [ ] Salvar com nomes corretos (oficina1.jpg, etc.)
- [ ] Testar no carrossel
- [ ] Adicionar créditos
- [ ] Verificar responsividade

## 🚀 Resultado Final

Quando implementado, o carrossel mostrará:
- ✅ Imagens reais da Oficina Jordão
- ✅ Créditos à oficina
- ✅ Design profissional
- ✅ Rotação automática
- ✅ Navegação intuitiva

---

**Nota:** As imagens atuais são temporárias do Unsplash. Substitua pelas da Oficina Jordão quando obtiver autorização. 