from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from .forms import RegistroForm, PerguntaRecuperacaoForm, RespostaSecretaForm, ResetSenhaForm
from .models import RespostaSecreta, PerguntaSecreta, TentativaRecuperacao
from .utils import hash_resposta, verificar_resposta, verificar_limite_tentativas, registrar_tentativa_erro, resetar_tentativas, get_client_ip

def register(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Salvar perguntas secretas
            perguntas = [
                form.cleaned_data.get('pergunta1'),
                form.cleaned_data.get('pergunta2'),
                form.cleaned_data.get('pergunta3')
            ]
            respostas = [
                form.cleaned_data.get('resposta1'),
                form.cleaned_data.get('resposta2'),
                form.cleaned_data.get('resposta3')
            ]
            
            for pergunta, resposta in zip(perguntas, respostas):
                if pergunta and resposta:
                    RespostaSecreta.objects.create(
                        user=user,
                        pergunta=pergunta,
                        resposta_hash=hash_resposta(resposta)
                    )
            
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('login')
        else:
            messages.error(request, 'Erro no cadastro. Verifique os dados.')
    else:
        form = RegistroForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def forgot_password(request):
    if request.method == 'POST':
        metodo = request.POST.get('metodo')
        
        if metodo == 'email':
            username = request.POST.get('username')
            try:
                user = User.objects.get(username=username)
                messages.success(request, 'Link de recuperação enviado para seu email!')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'Usuário não encontrado')
        
        elif metodo == 'perguntas':
            form = PerguntaRecuperacaoForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                try:
                    user = User.objects.get(username=username)
                    request.session['recovery_user_id'] = user.id
                    return redirect('verify_secret_questions')
                except User.DoesNotExist:
                    messages.error(request, 'Usuário não encontrado')
    
    return render(request, 'accounts/forgot_password.html')

def verify_secret_questions(request):
    return render(request, 'accounts/verify_secret_questions.html', {
        'pergunta': {'texto': 'Pergunta de teste'},
        'progresso': 33,
        'etapa_atual': 1,
        'total_etapas': 3
    })

def reset_password_secret(request):
    return render(request, 'accounts/reset_password_secret.html')

def recovery_success(request):
    return render(request, 'accounts/recovery_success.html')