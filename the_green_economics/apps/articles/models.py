from auditlog.registry import auditlog
from django.core.validators import FileExtensionValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from the_green_economics.apps.utils.models import Publication
from the_green_economics.apps.utils.models import PublicationTags


class ArticleTag(PublicationTags):
    """Model representing a tag for articles.

    Args:
        models (Model): Django model class.

    Attributes:
        name (CharField): Name of the article tag.
        slug (SlugField): Slug for the article tag, used in URLs.

    Returns:
        Model: ArticleTag instance.
    """

    class Meta:
        verbose_name = _("article tag")
        verbose_name_plural = _("article tags")
        indexes = [
            models.Index(fields=["tag"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return f"{self.tag} ({self.slug})"

    def get_absolute_url(self):
        return reverse("articles:tag_detail", kwargs={"slug": self.slug})

    def get_articles(self):
        return self.articles.all()


class Article(Publication):
    """Model representing an article.

    Attributes:
        title (CharField): Title of the article.
        slug (SlugField): Slug for the article, used in URLs.
        authors (CharField): Authors of the article.
        publication_date (DateField): Date of publication.
        abstract (TextField): Abstract of the article.
        body (TextField): Body content of the article.
        pdf (FileField): PDF file of the article.
        tags (ManyToManyField): Tags associated with the article.
        status (CharField): Status of the article (draft, published, etc.).
        created_at (DateTimeField): Date and time of creation.
        updated_at (DateTimeField): Date and time of last update.
        doi (CharField): Digital Object Identifier for the article.
        issn (CharField): International Standard Serial Number for the article.

    Returns:
        Model: Article instance.
    """

    pdf = models.FileField(
        verbose_name=_("article:model_pdf_verbose_name"),
        help_text=_("article:model_pdf_help_text"),
        upload_to="articles/pdfs/",
        validators=[FileExtensionValidator(["pdf"])],
        null=True,
    )
    tags = models.ManyToManyField(
        ArticleTag,
        verbose_name=_("article:model_tags_verbose_name"),
        help_text=_("article:model_tags_help_text"),
        related_name="articles",
    )
    doi = models.CharField(
        verbose_name=_("article:model_doi_verbose_name"),
        help_text=_("article:model_doi_help_text"),
        max_length=100,
        blank=True,
        default="",
    )
    issn = models.CharField(
        verbose_name=_("article:model_issn_verbose_name"),
        help_text=_("article:model_issn_help_text"),
        max_length=100,
        blank=True,
        default="",
    )

    class Meta:
        verbose_name = _("article:verbose_name")
        verbose_name_plural = _("article:verbose_name_plural")
        ordering = ["-publication_date"]
        indexes = [
            models.Index(fields=["publication_date"]),
            models.Index(fields=["status", "publication_date"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["doi"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.publication_date} - {self.status}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("articles:detail", kwargs={"slug": self.slug})


auditlog.register(Article)
auditlog.register(ArticleTag)
