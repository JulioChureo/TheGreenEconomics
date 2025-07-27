from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from the_green_economics.apps.contacts.models import ResearchProposal


@receiver(post_save, sender=ResearchProposal)
def research_proposal_post_save(sender, instance, created, **kwargs):
    if created:
        # Logic to execute after a new research proposal is created
        print(f"New research proposal created: {instance.title}")
    else:
        # Logic to execute after an existing research proposal is updated
        print(f"Research proposal updated: {instance.title}")
