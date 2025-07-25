from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Veiculo, Manutencao, Profissional

class UsuarioForm(UserCreationForm):
    """Formulário para cadastro e edição de usuários"""
    first_name = forms.CharField(
        label='Nome',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label='Sobrenome',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    telefone = forms.CharField(
        label='Telefone',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(11) 99999-9999'})
    )
    is_profissional = forms.BooleanField(
        label='Sou um profissional do setor automotivo',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    is_oficina = forms.BooleanField(
        label='Sou uma oficina/empresa automotiva',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'telefone', 'password1', 'password2', 'is_profissional', 'is_oficina')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar widgets
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        
        # Personalizar labels
        self.fields['username'].label = 'Nome de Usuário'
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Confirmar Senha'
        
        # Personalizar help_text
        self.fields['username'].help_text = 'Obrigatório. 150 caracteres ou menos. Letras, dígitos e @/./+/-/_ apenas.'
        self.fields['password1'].help_text = 'Sua senha deve conter pelo menos 8 caracteres.'
        self.fields['password2'].help_text = 'Digite a mesma senha novamente para verificação.'
        
    def clean(self):
        cleaned_data = super().clean()
        is_profissional = cleaned_data.get('is_profissional')
        is_oficina = cleaned_data.get('is_oficina')
        
        # Se marcou como oficina, automaticamente é profissional também
        if is_oficina:
            cleaned_data['is_profissional'] = True
            
        return cleaned_data

class VeiculoForm(forms.ModelForm):
    """Formulário para cadastro e edição de veículos"""
    class Meta:
        model = Veiculo
        fields = ['marca', 'modelo', 'ano', 'placa', 'km_atual']
        widgets = {
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'ano': forms.NumberInput(attrs={'class': 'form-control', 'min': '1900', 'max': '2030'}),
            'placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ABC-1234'}),
            'km_atual': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }
        labels = {
            'marca': 'Marca',
            'modelo': 'Modelo',
            'ano': 'Ano',
            'placa': 'Placa',
            'km_atual': 'Quilometragem Atual',
        }

class ManutencaoForm(forms.ModelForm):
    """Formulário para cadastro de manutenções"""
    class Meta:
        model = Manutencao
        fields = ['veiculo', 'servico', 'profissional', 'data', 'km', 'valor', 'observacoes']
        widgets = {
            'veiculo': forms.Select(attrs={'class': 'form-control'}),
            'servico': forms.Select(attrs={'class': 'form-control'}),
            'profissional': forms.Select(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'km': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'veiculo': 'Veículo',
            'servico': 'Serviço',
            'profissional': 'Profissional (opcional)',
            'data': 'Data',
            'km': 'Quilometragem',
            'valor': 'Valor (R$)',
            'observacoes': 'Observações',
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Se for profissional ou oficina, mostrar todos os veículos
            if user.is_profissional or user.is_oficina:
                self.fields['veiculo'].queryset = Veiculo.objects.all()
            else:
                # Filtrar veículos apenas do usuário logado
                self.fields['veiculo'].queryset = Veiculo.objects.filter(usuario=user)
            
            # Filtrar apenas profissionais aprovados
            self.fields['profissional'].queryset = self.fields['profissional'].queryset.filter(aprovado=True) 