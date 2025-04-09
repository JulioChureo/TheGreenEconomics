from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from the_green_economics.apps.users.models import User
