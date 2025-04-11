# public/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from Admin.models import JournalEntry
from django.views.generic import TemplateView


class JournalListView(ListView):
    """
    Vista para listar todas las entradas del journal.
    Solo muestra las publicaciones que están en estado 'publicado'.
    """
    model = JournalEntry
    template_name = 'journals/index.html'
    context_object_name = 'entries'
    paginate_by = 5

    def get_queryset(self):
        # Ajustar el filtro si `estado` no existe
        return JournalEntry.objects.filter(estado=True) 


class JournalDetailView(DetailView):
    """
    Vista para mostrar los detalles de una entrada específica.
    """
    model = JournalEntry
    template_name = 'journals/detail.html'
    context_object_name = 'entry'

    def get_object(self, queryset=None):
        return get_object_or_404(JournalEntry, slug=self.kwargs['slug'], estado='True')
    
class AboutView(TemplateView):
    template_name = 'about.html'  # Asegúrate que está en templates/about.html
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_members'] = [
            {'name': 'Juan Pérez', 'role': 'Fundador'},
            {'name': 'María García', 'role': 'Directora'},
            {'name': 'Carlos López', 'role': 'Diseñador'}
        ]
        return context