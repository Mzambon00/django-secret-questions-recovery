from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import RespostaSecreta, PerguntaSecreta
from .utils import hash_resposta

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Senha')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Confirmar Senha')
    
    pergunta1 = forms.ModelChoiceField(queryset=PerguntaSecreta.objects.filter(ativa=True), required=False, empty_label="Selecione uma pergunta")
    resposta1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    pergunta2 = forms.ModelChoiceField(queryset=PerguntaSecreta.objects.filter(ativa=True), required=False, empty_label="Selecione uma pergunta")
    resposta2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    pergunta3 = forms.ModelChoiceField(queryset=PerguntaSecreta.objects.filter(ativa=True), required=False, empty_label="Selecione uma pergunta")
    resposta3 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    usar_fallback = forms.BooleanField(required=False, initial=True, label='Usar como fallback de recovery')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean(self):
        cleaned_data = super().clean()
        perguntas = [cleaned_data.get('pergunta1'), cleaned_data.get('pergunta2'), cleaned_data.get('pergunta3')]
        respostas = [cleaned_data.get('resposta1'), cleaned_data.get('resposta2'), cleaned_data.get('resposta3')]
        
        # Se alguma pergunta foi preenchida, todas devem ser
        if any(perguntas) or any(respostas):
            for i, (pergunta, resposta) in enumerate(zip(perguntas, respostas), 1):
                if not pergunta:
                    self.add_error(f'pergunta{i}', 'Selecione uma pergunta')
                if not resposta:
                    self.add_error(f'resposta{i}', 'Digite uma resposta')
                if resposta and len(resposta) < 3:
                    self.add_error(f'resposta{i}', 'A resposta deve ter pelo menos 3 caracteres')
        
        # Verificar perguntas duplicadas
        perguntas_validas = [p for p in perguntas if p]
        if len(perguntas_validas) != len(set(perguntas_validas)):
            self.add_error(None, 'As perguntas devem ser diferentes entre si')
        
        return cleaned_data

class PerguntaRecuperacaoForm(forms.Form):
    username = forms.CharField(label='Usuário/Email', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

class RespostaSecretaForm(forms.Form):
    resposta = forms.CharField(label='Resposta', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
class ResetSenhaForm(forms.Form):
    nova_senha = forms.CharField(label='Nova Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirmar_senha = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    def clean(self):
        cleaned_data = super().clean()
        nova_senha = cleaned_data.get('nova_senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')
        
        if nova_senha and confirmar_senha and nova_senha != confirmar_senha:
            self.add_error('confirmar_senha', 'As senhas não conferem')
        
        if nova_senha and len(nova_senha) < 6:
            self.add_error('nova_senha', 'A senha deve ter pelo menos 6 caracteres')
        
        return cleaned_data
