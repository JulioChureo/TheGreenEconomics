from auditlog.registry import auditlog
from django.core.cache import cache
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class NewsTag(models.Model):
    name = models.CharField(_("news tag name"), max_length=50, unique=True)
    slug = models.SlugField(_("news tag slug"), max_length=50, unique=True)

    class Meta:
        verbose_name = _("news tag")
        verbose_name_plural = _("news tags")
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.name

    def get_articles(self):
        return self.news.all()


class News(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", _("Borrador")
        PUBLISHED = "PB", _("Publicado")
        ARCHIVED = "AR", _("Archivado")

    title = models.CharField(_("news title"), max_length=200, db_index=True)
    slug = models.SlugField(_("news slug"), max_length=200, unique=True)
    body = models.TextField(_("news content"))
    excerpt = models.CharField(_("news excerpt"), max_length=200, blank=True)
    featured_image = models.ImageField(
        _("new featured image"),
        upload_to="news/images/",
        blank=True,
        null=True,
    )
    publication_date = models.DateTimeField(
        _("new publication date"),
        default=timezone.now,
        db_index=True,
    )
    status = models.CharField(
        _("news status"),
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )
    tags = models.ManyToManyField(
        NewsTag,
        verbose_name=_("news tags"),
        related_name="news",
        blank=True,
    )
    created_at = models.DateTimeField(_("news creation date"), auto_now_add=True)
    updated_at = models.DateTimeField(_("news update date"), auto_now=True)

    class Meta:
        verbose_name = _("news item")
        verbose_name_plural = _("news")
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
