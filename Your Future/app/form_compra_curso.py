from django import forms
from .models import Vendas, Curso

class FormCompraCurso(forms.ModelForm):
    class Meta:
        model = Vendas
        fields = ('curso', 'quantidade')
        widgets = {
            'curso': forms.Select(attrs={

                'style': 'margin-bottom: 10px;',
            }),
            'quantidade': forms.NumberInput(attrs={
 
                'style': 'margin-bottom: 10px;',
                'min': 1,
            }),
        }
        labels = {
            'curso': 'Escolha o Curso',
            'quantidade': 'Quantidade',
        }
