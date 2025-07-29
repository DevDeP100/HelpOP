from django.core.management.base import BaseCommand
from core.models import TipoVeiculo, CategoriaChecklist, ItemChecklist

class Command(BaseCommand):
    help = 'Popula dados iniciais para o sistema de checklist'

    def handle(self, *args, **options):
        self.stdout.write('Criando tipos de veículos...')
        
        # Criar tipos de veículos
        tipos_veiculos = [
            {'nome': 'Carro', 'descricao': 'Automóveis de passeio'},
            {'nome': 'Moto', 'descricao': 'Motocicletas'},
            {'nome': 'Caminhão', 'descricao': 'Veículos de carga'},
            {'nome': 'Ônibus', 'descricao': 'Veículos de transporte coletivo'},
            {'nome': 'Van', 'descricao': 'Vans e utilitários'},
            {'nome': 'Caminhonete', 'descricao': 'Pick-ups e caminhonetes'},
        ]
        
        for tipo_data in tipos_veiculos:
            tipo, created = TipoVeiculo.objects.get_or_create(
                nome=tipo_data['nome'],
                defaults=tipo_data
            )
            if created:
                self.stdout.write(f'  ✓ Criado: {tipo.nome}')
            else:
                self.stdout.write(f'  - Já existe: {tipo.nome}')
        
        self.stdout.write('\nCriando categorias do checklist...')
        
        # Criar categorias do checklist
        categorias = [
            {'nome': 'Motor', 'descricao': 'Verificações do motor', 'ordem': 1},
            {'nome': 'Sistema de Freios', 'descricao': 'Verificações do sistema de freios', 'ordem': 2},
            {'nome': 'Suspensão', 'descricao': 'Verificações da suspensão', 'ordem': 3},
            {'nome': 'Sistema Elétrico', 'descricao': 'Verificações elétricas', 'ordem': 4},
            {'nome': 'Sistema de Arrefecimento', 'descricao': 'Verificações do sistema de arrefecimento', 'ordem': 5},
            {'nome': 'Sistema de Combustível', 'descricao': 'Verificações do sistema de combustível', 'ordem': 6},
            {'nome': 'Transmissão', 'descricao': 'Verificações da transmissão', 'ordem': 7},
            {'nome': 'Pneus e Rodas', 'descricao': 'Verificações de pneus e rodas', 'ordem': 8},
            {'nome': 'Iluminação', 'descricao': 'Verificações do sistema de iluminação', 'ordem': 9},
            {'nome': 'Segurança', 'descricao': 'Verificações de segurança', 'ordem': 10},
        ]
        
        for cat_data in categorias:
            categoria, created = CategoriaChecklist.objects.get_or_create(
                nome=cat_data['nome'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'  ✓ Criado: {categoria.nome}')
            else:
                self.stdout.write(f'  - Já existe: {categoria.nome}')
        
        self.stdout.write('\nCriando itens padrão do checklist...')
        
        # Criar itens padrão do checklist
        itens_padrao = [
            # Motor
            {'categoria': 'Motor', 'nome': 'Nível do óleo do motor', 'tipo_verificacao': 'visual', 'critico': True, 'ordem': 1},
            {'categoria': 'Motor', 'nome': 'Filtro de óleo', 'tipo_verificacao': 'visual', 'critico': False, 'ordem': 2},
            {'categoria': 'Motor', 'nome': 'Filtro de ar', 'tipo_verificacao': 'visual', 'critico': False, 'ordem': 3},
            {'categoria': 'Motor', 'nome': 'Correias do motor', 'tipo_verificacao': 'visual', 'critico': True, 'ordem': 4},
            {'categoria': 'Motor', 'nome': 'Vazamentos', 'tipo_verificacao': 'visual', 'critico': True, 'ordem': 5},
            
            # Sistema de Freios
            {'categoria': 'Sistema de Freios', 'nome': 'Nível do fluido de freio', 'tipo_verificacao': 'visual', 'critico': True, 'ordem': 1},
            {'categoria': 'Sistema de Freios', 'nome': 'Pastilhas de freio', 'tipo_verificacao': 'visual', 'critico': True, 'ordem': 2},
            {'categoria': 'Sistema de Freios', 'nome': 'Discos de freio', 'tipo_verificacao': 'visual', 'critico': True, 'ordem': 3},
            {'categoria': 'Sistema de Freios', 'nome': 'Cilindros de freio', 'tipo_verificacao': 'teste', 'critico': True, 'ordem': 4},
            {'categoria': 'Sistema de Freios', 'nome': 'Cabo do freio de mão', 'tipo_verificacao': 'teste', 'critico': True, 'ordem': 5},
            
            # Suspensão
            {'categoria': 'Suspensão', 'nome': 'Amortecedores', 'tipo_verificacao': 'teste', 'critico': True, 'ordem': 1},
            {'categoria': 'Suspensão', 'nome': 'Molas', 'tipo_verificacao': 'visual', 'critico': False, 'ordem': 2},
            {'categoria': 'Suspensão', 'nome': 'Buchas da suspensão', 'tipo_verificacao': 'teste', 'critico': True, 'ordem': 3},
            {'categoria': 'Suspensão', 'nome': 'Bandejas', 'tipo_verificacao': 'visual', 'critico': True, 'ordem': 4},
            
            # Sistema Elétrico
            {'categoria': 'Sistema Elétrico', 'nome': 'Bateria', 'tipo_verificacao': 'teste', 'critico': True, 'ordem': 1},
            {'categoria': 'Sistema Elétrico', 'nome': 'Alternador', 'tipo_verificacao': 'teste', 'critico': True, 'ordem': 2},
            {'categoria': 'Sistema Elétrico', 'nome': 'Motor de partida', 'tipo_verificacao': 'teste', 'critico': True, 'ordem': 3},
            {'categoria': 'Sistema Elétrico', 'nome': 'Fusíveis', 'tipo_verificacao': 'visual', 'critico': False, 'ordem': 4},
            
            # Sistema de Arrefecimento
            {'categoria': 'Sistema de Arrefecimento', 'nome': 'Nível do líquido de arrefecimento', 'tipo_verificacao': 'visual', 'critico': True, 'ordem': 1},
            {'categoria': 'Sistema de Arrefecimento', 'nome': 'Radiador', 'tipo_verificacao': 'visual', 'critico': True, 'ordem': 2},
            {'categoria': 'Sistema de Arrefecimento', 'nome': 'Mangueiras', 'tipo_verificacao': 'visual', 'critico': True, 'ordem': 3},
            {'categoria': 'Sistema de Arrefecimento', 'nome': 'Bomba d\'água', 'tipo_verificacao': 'teste', 'critico': True, 'ordem': 4},
            
            # Sistema de Combustível
            {'categoria': 'Sistema de Combustível', 'nome': 'Filtro de combustível', 'tipo_verificacao': 'visual', 'critico': False, 'ordem': 1},
            {'categoria': 'Sistema de Combustível', 'nome': 'Bomba de combustível', 'tipo_verificacao': 'teste', 'critico': True, 'ordem': 2},
            {'categoria': 'Sistema de Combustível', 'nome': 'Bicos injetores', 'tipo_verificacao': 'teste', 'critico': True, 'ordem': 3},
            
            # Transmissão
            {'categoria': 'Transmissão', 'nome': 'Nível do óleo da transmissão', 'tipo_verificacao': 'visual', 'critico': True, 'ordem': 1},
            {'categoria': 'Transmissão', 'nome': 'Embreagem', 'tipo_verificacao': 'teste', 'critico': True, 'ordem': 2},
            {'categoria': 'Transmissão', 'nome': 'Diferencial', 'tipo_verificacao': 'visual', 'critico': True, 'ordem': 3},
            
            # Pneus e Rodas
            {'categoria': 'Pneus e Rodas', 'nome': 'Pressão dos pneus', 'tipo_verificacao': 'medicao', 'critico': True, 'ordem': 1},
            {'categoria': 'Pneus e Rodas', 'nome': 'Desgaste dos pneus', 'tipo_verificacao': 'visual', 'critico': True, 'ordem': 2},
            {'categoria': 'Pneus e Rodas', 'nome': 'Alinhamento', 'tipo_verificacao': 'teste', 'critico': False, 'ordem': 3},
            {'categoria': 'Pneus e Rodas', 'nome': 'Balanceamento', 'tipo_verificacao': 'teste', 'critico': False, 'ordem': 4},
            
            # Iluminação
            {'categoria': 'Iluminação', 'nome': 'Faróis', 'tipo_verificacao': 'teste', 'critico': True, 'ordem': 1},
            {'categoria': 'Iluminação', 'nome': 'Lanternas', 'tipo_verificacao': 'teste', 'critico': True, 'ordem': 2},
            {'categoria': 'Iluminação', 'nome': 'Seta direcional', 'tipo_verificacao': 'teste', 'critico': True, 'ordem': 3},
            {'categoria': 'Iluminação', 'nome': 'Luz de freio', 'tipo_verificacao': 'teste', 'critico': True, 'ordem': 4},
            
            # Segurança
            {'categoria': 'Segurança', 'nome': 'Cintos de segurança', 'tipo_verificacao': 'teste', 'critico': True, 'ordem': 1},
            {'categoria': 'Segurança', 'nome': 'Airbags', 'tipo_verificacao': 'teste', 'critico': True, 'ordem': 2},
            {'categoria': 'Segurança', 'nome': 'Extintor', 'tipo_verificacao': 'visual', 'critico': True, 'ordem': 3},
            {'categoria': 'Segurança', 'nome': 'Triângulo de segurança', 'tipo_verificacao': 'visual', 'critico': True, 'ordem': 4},
        ]
        
        for item_data in itens_padrao:
            categoria = CategoriaChecklist.objects.get(nome=item_data['categoria'])
            item, created = ItemChecklist.objects.get_or_create(
                categoria=categoria,
                nome=item_data['nome'],
                defaults={
                    'tipo_verificacao': item_data['tipo_verificacao'],
                    'critico': item_data['critico'],
                    'ordem': item_data['ordem']
                }
            )
            if created:
                self.stdout.write(f'  ✓ Criado: {item.categoria.nome} - {item.nome}')
            else:
                self.stdout.write(f'  - Já existe: {item.categoria.nome} - {item.nome}')
        
        self.stdout.write(self.style.SUCCESS('\n✓ Dados iniciais do checklist criados com sucesso!'))
        self.stdout.write('\nResumo:')
        self.stdout.write(f'  - {TipoVeiculo.objects.count()} tipos de veículos')
        self.stdout.write(f'  - {CategoriaChecklist.objects.count()} categorias')
        self.stdout.write(f'  - {ItemChecklist.objects.count()} itens padrão') 