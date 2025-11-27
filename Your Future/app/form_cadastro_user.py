from django import forms
from app.models import Usuario

class FormCadastroUser(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nome', 'email', 'senha', 'foto')
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Nome',
                'class': 'form-control',
                'style': 'margin-bottom: 10px;'  
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email',
                'class': 'form-control',
                'style': 'margin-bottom: 10px;'
            }),
            'senha': forms.PasswordInput(attrs={
                'placeholder': 'Senha',
                'class': 'form-control',
                'style': 'margin-bottom: 10px;'
            }),
            'foto': forms.FileInput(attrs={
                'accept': 'image/*',
                'placeholder': 'Foto',
                'class': 'form-control',
                'style': 'margin-bottom: 10px;'
            }),
        }

        error_messages = {
            'email': {
                'required': "Insira um e-mail.",
                'unique': "Esse e-mail já está cadastrado.", 
            },
            'senha': {
                'required': "Insira uma senha.",
            },
        }
