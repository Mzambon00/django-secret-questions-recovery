# Criar README.md foda
@'
<div align="center">

# 🔐 DJSQR - Django Secret Questions Recovery

### *Sistema de Recuperação de Conta com Fallback de Perguntas Secretas*

[![Django Version](https://img.shields.io/badge/Django-4.2-092e20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.14-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-ff69b4?style=for-the-badge&logo=mit&logoColor=white)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Mzambon00/django-secret-questions-recovery)

![Status](https://img.shields.io/badge/STATUS-EM%20DESENVOLVIMENTO-green?style=for-the-badge)
![Security](https://img.shields.io/badge/SECURITY-ENHANCED-red?style=for-the-badge)
![Privacy](https://img.shields.io/badge/PRIVACY-FIRST-blue?style=for-the-badge)

</div>

---

## 🎯 **Sobre o Projeto**

Em um mundo onde **acesso ao email não é garantido**, este sistema oferece uma camada extra de segurança para recuperação de contas. Desenvolvido com **melhores práticas de segurança**, permite que usuários recuperem suas contas através de **perguntas secretas** quando o método tradicional de email falha.

### 🔥 **Diferenciais**

| Característica | Descrição |
|----------------|-----------|
| 🛡️ **Zero Plain Text** | Respostas nunca são armazenadas em texto puro |
| 🧂 **Salt Unique** | Hash SHA-256 com salt único por resposta |
| 🚦 **Rate Limiting** | 3 tentativas/hora + bloqueio de 15min |
| 📊 **Wizard UX** | Interface passo-a-passo com barra de progresso |
| 🎨 **Modern Design** | Gradientes, animações e responsivo |

---

## ✨ **Funcionalidades**

### 👤 **Para Usuários**
- ✅ Cadastro com perguntas secretas (opcional)
- ✅ Recuperação via email (NTFY)
- ✅ Recuperação via perguntas secretas
- ✅ Redefinição segura de senha
- ✅ Interface guiada passo-a-passo

### 🔒 **Para Administradores**
- ✅ Logs de tentativas suspeitas
- ✅ Controle de tentativas por IP
- ✅ Gerenciamento de perguntas pelo admin
- ✅ Monitoramento de bloqueios

---

## 🏗️ **Arquitetura de Segurança**
