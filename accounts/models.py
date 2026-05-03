from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import hashlib
import secrets

class PerguntaSecreta(models.Model):
    texto = models.CharField(max_length=200)
    ativa = models.BooleanField(default=True)
    ordem = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['ordem', 'id']
        verbose_name = 'Pergunta Secreta'
        verbose_name_plural = 'Perguntas Secretas'
    
    def __str__(self):
        return self.texto

class RespostaSecreta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='respostas_secretas')
    pergunta = models.ForeignKey(PerguntaSecreta, on_delete=models.CASCADE)
    resposta_hash = models.CharField(max_length=255)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'pergunta']
        verbose_name = 'Resposta Secreta'
        verbose_name_plural = 'Respostas Secretas'
    
    def __str__(self):
        return f"{self.user.username} - {self.pergunta.texto[:30]}"

class TentativaRecuperacao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tentativas_recuperacao')
    ip_address = models.GenericIPAddressField()
    tentativas = models.IntegerField(default=0)
    bloqueado_ate = models.DateTimeField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Tentativa de Recuperação'
        verbose_name_plural = 'Tentativas de Recuperação'
    
    def __str__(self):
        return f"{self.user.username} - {self.tentativas} tentativas"

class LogTentativaSuspeita(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logs_suspeitos')
    ip_address = models.GenericIPAddressField()
    acao = models.CharField(max_length=100)
    detalhes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Log de Tentativa Suspeita'
        verbose_name_plural = 'Logs de Tentativas Suspeitas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"{self.user.username} - {self.acao} - {self.criado_em}"
