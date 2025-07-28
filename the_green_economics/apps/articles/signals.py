from django.core.cache import cache
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch import receiver
from requests import delete

from the_green_economics.apps.articles.models import Article

CACHE_ARTICLE_KEYS = ()


@receiver(post_save, sender=Article)
def article_post_save(sender, instance: Article, created, **kwargs):
    """cache invalidation signal for article save"""
    cache.delete("articles:home_articles")


@receiver(post_delete, sender=Article)
def article_pre_delete(sender, instance: Article, **kwargs):
    """cache invalidation signal for article delete"""
    cache.delete("articles:home_articles")
