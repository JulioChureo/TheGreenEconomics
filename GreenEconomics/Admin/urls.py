# management/urls.py
from django.urls import path
from .views import (
    admin_login, admin_dashboard, admin_logout, create_journal, edit_journal, delete_journal
)

urlpatterns = [
    path('login/', admin_login, name='admin_login'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('logout/', admin_logout, name='admin_logout'),
    path('create/', create_journal, name='create_journal'),
    path('edit/<int:pk>/', edit_journal, name='edit_journal'),
    path('delete/<int:pk>/', delete_journal, name='delete_journal'),
]
