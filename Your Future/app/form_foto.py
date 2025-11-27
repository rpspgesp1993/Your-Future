from django import forms
from app.models import Foto

class FormFoto(forms.ModelForm):    
    class Meta:
        model = Foto 
        fields = ['nome', 'foto']

        widgets = {
            'foto': forms.FileInput(attrs={'accept' : 'image/*'})
        }
