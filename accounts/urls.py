from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('registrar/', views.register, name='register'),
    path('esqueci-senha/', views.forgot_password, name='forgot_password'),
    path('verificar-perguntas/', views.verify_secret_questions, name='verify_secret_questions'),
    path('resetar-senha-secreta/', views.reset_password_secret, name='reset_password_secret'),
    path('recuperacao-sucesso/', views.recovery_success, name='recovery_success'),
]
