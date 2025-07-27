from django.urls import path

from the_green_economics.apps.contacts.views import research_proposal_create_view

app_name = "contacts"

urlpatterns = [
    path(
        "publish/",
        research_proposal_create_view,
        name="create",
    ),
]
