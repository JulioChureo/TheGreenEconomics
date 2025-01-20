# admin/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import View
from Admin.models import JournalEntry
from Admin.forms import JournalForm


def admin_login(request):
    """
    Vista para manejar el inicio de sesión administrativo.
    Solo permite el acceso a usuarios con permisos de staff.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Credenciales inválidas o usuario no autorizado.')
    return render(request, 'admin/login.html')


@login_required
def admin_dashboard(request):
    """
    Vista para el panel de administración.
    Solo accesible para usuarios autenticados con permisos de staff.
    """
    if not request.user.is_staff:
        return redirect('admin_login')
    journals = JournalEntry.objects.all().order_by('-fecha_creacion')
    return render(request, 'admin/dashboard.html', {'journals': journals})


@login_required
def admin_logout(request):
    """
    Vista para cerrar la sesión del usuario administrativo.
    """
    logout(request)
    return redirect('admin_login')



@login_required
def create_journal(request):
    """
    Vista para crear una nueva entrada en el journal.
    """
    if not request.user.is_staff:
        return redirect('admin_login')

    if request.method == 'POST':
        form = JournalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entrada creada exitosamente.')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Ocurrió un error al guardar la entrada.')
    else:
        form = JournalForm()

    return render(request, 'admin/create_journal.html', {'form': form})


@login_required
def edit_journal(request, pk):
    """
    Vista para editar una entrada existente en el journal.
    """
    if not request.user.is_staff:
        return redirect('admin_login')

    journal = get_object_or_404(JournalEntry, pk=pk)
    if request.method == 'POST':
        form = JournalForm(request.POST, request.FILES, instance=journal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entrada actualizada exitosamente.')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Ocurrió un error al actualizar la entrada.')
    else:
        form = JournalForm(instance=journal)

    return render(request, 'admin/edit_journal.html', {'form': form, 'journal': journal})


@login_required
def delete_journal(request, pk):
    """
    Vista para eliminar una entrada en el journal.
    """
    if not request.user.is_staff:
        return redirect('admin_login')

    journal = get_object_or_404(JournalEntry, pk=pk)
    if request.method == 'POST':
        journal.delete()
        messages.success(request, 'Entrada eliminada exitosamente.')
        return redirect('admin_dashboard')

    return render(request, 'admin/delete_journal.html', {'journal': journal})
