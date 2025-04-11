# public/urls.py
from django.urls import path
from .views import JournalListView, JournalDetailView,AboutView

urlpatterns = [
    path('', JournalListView.as_view(), name='journal_list'),
    path('<slug:slug>/', JournalDetailView.as_view(), name='journal_detail'),
]
