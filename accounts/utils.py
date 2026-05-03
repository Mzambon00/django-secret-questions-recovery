import hashlib
import secrets
from django.utils import timezone
from datetime import timedelta
from .models import TentativaRecuperacao, LogTentativaSuspeita

def hash_resposta(resposta: str, salt: str = None) -> str:
    if salt is None:
        salt = secrets.token_hex(16)
    
    resposta_com_salt = f"{resposta.lower().strip()}{salt}"
    hash_obj = hashlib.sha256(resposta_com_salt.encode('utf-8'))
    hash_final = f"{salt}${hash_obj.hexdigest()}"
    
    return hash_final

def verificar_resposta(resposta: str, hash_armazenado: str) -> bool:
    try:
        salt, hash_original = hash_armazenado.split('$')
        hash_verificar = hash_resposta(resposta, salt)
        return hash_verificar == hash_armazenado
    except:
        return False

def verificar_limite_tentativas(user, request) -> tuple:
    ip_address = get_client_ip(request)
    
    tentativa, created = TentativaRecuperacao.objects.get_or_create(
        user=user,
        ip_address=ip_address,
        defaults={'tentativas': 0, 'bloqueado_ate': None}
    )
    
    if tentativa.bloqueado_ate and tentativa.bloqueado_ate > timezone.now():
        tempo_restante = (tentativa.bloqueado_ate - timezone.now()).seconds // 60
        return False, f"Você excedeu o limite de tentativas. Tente novamente em {tempo_restante} minutos.", tentativa
    
    if tentativa.bloqueado_ate and tentativa.bloqueado_ate <= timezone.now():
        tentativa.tentativas = 0
        tentativa.bloqueado_ate = None
        tentativa.save()
    
    return True, "", tentativa

def registrar_tentativa_erro(user, request, tentativa_obj):
    tentativa_obj.tentativas += 1
    
    if tentativa_obj.tentativas >= 3:
        tentativa_obj.bloqueado_ate = timezone.now() + timedelta(minutes=15)
        registrar_log_suspeito(user, request, "muitas_tentativas", f"{tentativa_obj.tentativas} tentativas falhas")
    
    tentativa_obj.save()

def resetar_tentativas(user, request):
    ip_address = get_client_ip(request)
    TentativaRecuperacao.objects.filter(user=user, ip_address=ip_address).delete()

def registrar_log_suspeito(user, request, acao, detalhes=""):
    ip_address = get_client_ip(request)
    LogTentativaSuspeita.objects.create(
        user=user,
        ip_address=ip_address,
        acao=acao,
        detalhes=detalhes
    )

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
