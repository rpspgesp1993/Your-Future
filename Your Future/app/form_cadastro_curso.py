from django import forms
from app.models import Curso

class FormCadastroCurso(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ('nome', 'autor', 'duracao', 'preco', 'foto', 'quantidade_estoque')  # Campo adicionado
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Nome do Curso',
                'class': 'form-control',
                'style': 'margin-bottom: 10px;'
            }),
            'autor': forms.TextInput(attrs={
                'placeholder': 'Autor do Curso',
                'class': 'form-control',
                'style': 'margin-bottom: 10px;'
            }),
            'duracao': forms.NumberInput(attrs={
                'placeholder': 'Duração (horas)',
                'class': 'form-control',
                'style': 'margin-bottom: 10px;'
            }),
            'preco': forms.NumberInput(attrs={
                'placeholder': 'Preço',
                'step': '0.01',
                'class': 'form-control',
                'style': 'margin-bottom: 10px;'
            }),
            'foto': forms.FileInput(attrs={
                'accept': 'image/*',
                'placeholder': 'Foto',
                'class': 'form-control',
                'style': 'margin-bottom: 10px;'
            }),
            'quantidade_estoque': forms.NumberInput(attrs={  # Novo widget
                'placeholder': 'Quantidade em Estoque',
                'class': 'form-control',
                'style': 'margin-bottom: 10px;',
                'min': 0  # Garante que não sejam inseridos valores negativos
            }),
        }

        error_messages = {
            'nome': {
                'required': "Insira o nome do curso.",
            },
            'autor': {
                'required': "Insira o autor do curso.",
            },
            'duracao': {
                'required': "Insira a duração do curso.",
            },
            'preco': {
                'required': "Insira o preço do curso.",
            },
            'quantidade_estoque': {
                'required': "Insira a quantidade em estoque.",
                'min_value': "A quantidade não pode ser negativa.",
            },
        }
