from django import forms
from app.models import Login, Usuario

class FormLogin(forms.ModelForm):
    class Meta:
        model = Login
        fields = ('email', 'senha')

        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control', 'type': 'email'}),  
            'senha': forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}), 
        }
