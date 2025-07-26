from auditlog.registry import auditlog
from django.core.cache import cache
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from the_green_economics.apps.utils.models import Publication
from the_green_economics.apps.utils.models import PublicationTags


class NewsTag(PublicationTags):
    class Meta:
        verbose_name = _("news_tag:model_verbose_name")
        verbose_name_plural = _("news_tag:model_verbose_name_plural")
        indexes = [
            models.Index(fields=["tag"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return f"{self.tag} ({self.slug})"

    def get_articles(self):
        return self.news.all()


class News(Publication):
    excerpt = models.CharField(
        verbose_name=_("news:model_excerpt_verbose_name"),
        help_text=_("news:model_excerpt_help_text"),
        max_length=200,
        blank=True,
    )
    featured_image = models.ImageField(
        verbose_name=_("news:model_featured_image_verbose_name"),
        help_text=_("news:model_featured_image_help_text"),
        upload_to="news/images/",
        null=True,
    )
    tags = models.ManyToManyField(
        NewsTag,
        verbose_name=_("news:model_tags_verbose_name"),
        help_text=_("news:model_tags_help_text"),
        related_name="news",
        blank=True,
    )

    class Meta:
        verbose_name = _("news:model_verbose_name")
        verbose_name_plural = _("news:model_verbose_name_plural")
        ordering = ["-publication_date"]
        indexes = [
            models.Index(fields=["publication_date", "status"]),
            models.Index(fields=["slug", "status"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        # Invalidar cache al guardar
        cache.delete_many(["latest_news", "featured_news", f"news_{self.slug}"])
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("news:detail", kwargs={"slug": self.slug})

    def generate_unique_slug(self):
        base_slug = slugify(self.title)
        unique_slug = base_slug
        counter = 1
        while News.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{counter}"
            counter += 1
        return unique_slug


# Register the models with auditlog
auditlog.register(News)
auditlog.register(NewsTag)
