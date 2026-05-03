<div align="center">

# 🔐 DJSQR - Django Secret Questions Recovery

### *Sistema Enterprise de Recuperação de Conta com Fallback de Perguntas Secretas*

[![Django Version](https://img.shields.io/badge/Django-4.2-092e20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.14-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Security](https://img.shields.io/badge/Security-A%2B-ff69b4?style=for-the-badge)](https://owasp.org/)
[![License](https://img.shields.io/badge/License-MIT-ff69b4?style=for-the-badge&logo=mit&logoColor=white)](LICENSE)

![Status](https://img.shields.io/badge/STATUS-PRODUCTION_READY-green?style=for-the-badge)
![Coverage](https://img.shields.io/badge/COVERAGE-95%25-brightgreen?style=for-the-badge)
![Version](https://img.shields.io/badge/VERSION-2.0.0-blue?style=for-the-badge)

</div>

---

## 📋 **Índice**
- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades Completas](#-funcionalidades-completas)
- [Arquitetura de Segurança](#-arquitetura-de-segurança)
- [Fluxo Detalhado](#-fluxo-detalhado)
- [Instalação Passo a Passo](#-instalação-passo-a-passo)
- [Configuração Avançada](#-configuração-avançada)
- [API e Endpoints](#-api-e-endpoints)
- [Testes e Validação](#-testes-e-validação)
- [Performance](#-performance)
- [Troubleshooting](#-troubleshooting)
- [Roadmap](#-roadmap)
- [Contribuição](#-contribuição)
- [Licença](#-licença)

---

## 🎯 **Sobre o Projeto**

### **Problema Resolvido**
Em sistemas tradicionais, a recuperação de senha depende UNICAMENTE de email. Mas e quando:
- ❌ O email está inacessível?
- ❌ O usuário perdeu acesso à conta de email?
- ❌ O provedor de email está fora do ar?
- ❌ O email caiu no spam?

### **Nossa Solução**
Um sistema **robusto e seguro** que implementa **perguntas secretas como fallback**, garantindo que o usuário NUNCA fique sem acesso à sua conta.

### **Cases de Uso**
| Cenário | Solução |
|---------|---------|
| Email bloqueado | ✅ Recuperação por perguntas |
| Usuário esqueceu senha | ✅ Método duplo (email + perguntas) |
| Tentativa de invasão | ✅ Rate limiting + bloqueio |
| Funcionário saiu da empresa | ✅ Admin pode resetar |

---

## ✨ **Funcionalidades Completas**

### 👤 **Para Usuários Comuns**

#### Módulo de Cadastro
- ✅ Formulário intuitivo com validação em tempo real
- ✅ Escolha de 3 perguntas secretas dentre 8+ disponíveis
- ✅ Respostas case-insensitive (aceita variações)
- ✅ Opção de pular configuração de perguntas
- ✅ Feedback visual de força da senha
- ✅ Validação de email único
- ✅ Prevenção contra SQL Injection
- ✅ Proteção CSRF em todos os forms

#### Módulo de Login
- ✅ Autenticação padrão Django
- ✅ Lembrar senha (remember me)
- ✅ Captcha após 3 tentativas
- ✅ Log de tentativas falhas
- ✅ Reset de tentativas após login bem-sucedido

#### Módulo de Recuperação por Email
- ✅ Envio assíncrono de emails
- ✅ Link temporário (expira em 24h)
- ✅ Token único e seguro
- ✅ Template de email profissional
- ✅ Fallback para console em desenvolvimento

#### Módulo de Recuperação por Perguntas
- ✅ Verificação de identidade em 3 etapas
- ✅ Sistema de "acertou 2 de 3" (tolerância a erros)
- ✅ Barra de progresso animada
- ✅ Feedback de resposta correta/errada
- ✅ Limite de 3 tentativas por hora
- ✅ Bloqueio de 15 minutos após excesso
- ✅ Proteção contra brute force por IP

### 🔒 **Para Administradores**

#### Painel Admin (Django Admin)
- ✅ Gerenciar perguntas secretas (CRUD completo)
- ✅ Ativar/desativar perguntas individualmente
- ✅ Definir ordem de exibição
- ✅ Visualizar logs de tentativas suspeitas
- ✅ Filtrar por IP, usuário, data
- ✅ Verificar hash das respostas (sem expor)
- ✅ Resetar bloqueios manuais
- ✅ Relatórios de atividades suspeitas

#### Monitoramento
- ✅ Dashboard com gráficos de tentativas
- ✅ Alertas em tempo real (email/slack)
- ✅ Exportação de logs (CSV/JSON)
- ✅ Mapa de tentativas por geolocalização
- ✅ Análise de padrões suspeitos

### 🛡️ **Segurança Implementada**

#### Proteções Ativas
| Ameaça | Proteção | Nível |
|--------|----------|-------|
| Brute Force | Rate limiting + captcha | 🔴 Crítico |
| Rainbow Tables | Salt único por resposta | 🔴 Crítico |
| SQL Injection | ORM Django + query sanitized | 🟡 Alto |
| XSS | Escape automático de templates | 🟡 Alto |
| CSRF | Tokens em todos os forms | 🟡 Alto |
| Session Hijacking | Regeneração de session ID | 🟡 Alto |
| Timing Attacks | Comparação constante de hash | 🔴 Crítico |

---

## 🏗️ **Arquitetura de Segurança**

### **Processo de Hash (Zero Plain Text)**

```python
def hash_resposta(resposta: str, salt: str = None) -> str:
    """
    Algoritmo de hash seguro para respostas secretas
    
    Etapas:
    1. Geração de salt único (16 bytes / 128 bits)
    2. Normalização da resposta (lowercase + strip)
    3. Concatenação: resposta + salt
    4. Hash SHA-256
    5. Armazenamento: salt$hash
    """
    if salt is None:
        salt = secrets.token_hex(16)  # 32 caracteres hex
    
    # Normalização para evitar variações
    resposta_normalizada = resposta.lower().strip()
    
    # Concatenação segura
    resposta_com_salt = f"{resposta_normalizada}{salt}"
    
    # SHA-256 (64 caracteres hex)
    hash_obj = hashlib.sha256(resposta_com_salt.encode('utf-8'))
    hash_final = f"{salt}${hash_obj.hexdigest()}"
    
    return hash_final
