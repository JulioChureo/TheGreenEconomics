from django.core.validators import FileExtensionValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class ArticleTag(models.Model):
    name = models.CharField(_("article tag name"), max_length=50, unique=True)
    slug = models.SlugField(_("article tag slug"), max_length=50, unique=True)

    class Meta:
        verbose_name = _("article tag")
        verbose_name_plural = _("article tags")
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.name

    def get_articles(self):
        return self.articles.all()


class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", _("Borrador")
        PUBLISHED = "PB", _("Publicado")
        UNDER_REVIEW = "UR", _("En revisión")

    title = models.CharField(_("article title"), max_length=200)
    slug = models.SlugField(_("article slug"), max_length=200, unique=True)
    authors = models.CharField(_("article authors"), max_length=200, blank=True)
    publication_date = models.DateField(
        _("article publication date"),
        blank=True,
        null=True,
    )

    abstract = models.TextField(_("article abstract"))
    body = models.TextField(_("article body"))
    pdf = models.FileField(
        _("archivo PDF"),
        upload_to="articles/pdfs/",
        validators=[FileExtensionValidator(["pdf"])],
    )
    tags = models.ManyToManyField(
        ArticleTag,
        verbose_name=_("etiquetas"),
        related_name="articles",
        blank=True,
    )
    status = models.CharField(
        _("article status"),
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    created_at = models.DateTimeField(_("fecha de creación"), auto_now_add=True)
    updated_at = models.DateTimeField(_("fecha de actualización"), auto_now=True)

    class Meta:
        verbose_name = _("artículo científico")
        verbose_name_plural = _("artículos científicos")
        ordering = ["-publication_date"]
        indexes = [
            models.Index(fields=["publication_date"]),
            models.Index(fields=["status", "publication_date"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.publication_date} - {self.status}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("articles:detail", kwargs={"slug": self.slug})
