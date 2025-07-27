from typing import Any

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django_tasks import task


@task(queue_name="email", priority=1, enqueue_on_commit=True)
def send_admin_proposal_email(proposal: dict[str, Any]):
    """Send an email to the admin when a ResearchProposal is created."""
    # Render the plain text content.
    text_content = render_to_string(
        "emails/contacts/admin_contact.txt",
        context={"proposal": proposal},
    )

    # Create a multipart email instance.
    msg = EmailMultiAlternatives(
        subject="Nueva Propuesta de Investigación Recibida",
        body=text_content,
        from_email=settings.MANAGERS[1][1],
        to=[settings.MANAGERS[1][1]],
    )

    msg.send()


@task(queue_name="email", priority=1, enqueue_on_commit=True)
def send_user_proposal_email(proposal: dict[str, Any]):
    """Send an email to the user when a ResearchProposal is created."""
    # Render the plain text content.
    text_content = render_to_string(
        "emails/contacts/sender_contact.txt",
        context={"proposal": proposal},
    )

    # Create a multipart email instance.
    msg = EmailMultiAlternatives(
        subject="Confirmación de Recepción de Propuesta",
        body=text_content,
        from_email=settings.MANAGERS[1][1],
        to=[proposal["email"]],
    )

    msg.send()
