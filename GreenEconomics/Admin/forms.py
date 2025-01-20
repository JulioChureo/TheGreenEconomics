from django import forms
from Admin.models import JournalEntry

class JournalForm(forms.ModelForm):
    """
    Formulario para crear y editar entradas del journal.
    """
    class Meta:
        model = JournalEntry
        fields = ['titulo', 'content']  # Se elimina el campo 'slug'
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título de la entrada',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Contenido de la entrada',
                'rows': 10,
            }),
        }
        labels = {
            'titulo': 'Título',
            'content': 'Contenido',
        }
