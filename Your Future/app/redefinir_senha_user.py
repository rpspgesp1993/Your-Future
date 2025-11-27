from django import forms 
from app.models import Usuario
from django.contrib.auth.forms import PasswordChangeForm

class RedefinirSenhaUser(PasswordChangeForm ):
    model = Usuario;
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite sua senha antiga',
            'class': 'form-control',
        }),
        label="Senha antiga"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite a nova senha',
            'class': 'form-control',
        }),
        label="Nova senha"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme a nova senha',
            'class': 'form-control',
        }),
        label="Confirme a nova senha"
    )
