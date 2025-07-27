from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.template.loader import render_to_string

from the_green_economics.apps.contacts.models import ResearchProposal
from the_green_economics.apps.contacts.tasks import send_admin_proposal_email
from the_green_economics.apps.contacts.tasks import send_user_proposal_email


@receiver(post_save, sender=ResearchProposal)
def research_proposal_post_save(sender, instance: ResearchProposal, created, **kwargs):
    """Signal to handle actions after a ResearchProposal is saved.
    send a email to the email on the proposal and a email to the admin

    Args:
        sender (_type_): _description_
        instance (_type_): _description_
        created (_type_): _description_
    """

    if not created:
        return

    json_instance = instance.to_dict()

    admin_task_id = send_admin_proposal_email.enqueue(proposal=json_instance)
    user_task_id = send_user_proposal_email.enqueue(proposal=json_instance)
