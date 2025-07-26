from django.db import models
from django.utils.translation import gettext_lazy as _


class PublicationStatus(models.TextChoices):
    """Enumeration for publication statuses.

    Attributes:
        DRAFT (str): Represents a draft publication.
        PUBLISHED (str): Represents a published publication.
        UNDER_REVIEW (str): Represents a publication that is under review.
        ARCHIVED (str): Represents an archived publication.
    """

    DRAFT = "DF", _("publication:status_draft")
    PUBLISHED = "PB", _("publication:status_published")
    UNDER_REVIEW = "UR", _("publication:status_under_review")
    ARCHIVED = "AR", _("publication:status_archived")


class PublicationTags(models.Model):
    """Base model for publication tags in the Green Economics app.
    This model serves as a base for tags associated with articles, blog posts, and other
    types of content.

    Attributes:
        slug (str): A unique identifier for the tag.
        tag (str): The name of the tag.

    Example:
        >>> tag = PublicationTags(slug="environment", tag="Environment")
        >>> tag.save()
    """

    slug = models.SlugField(
        verbose_name=_("publication:model_slug_verbose_name"),
        help_text=_("publication:model_slug_help_text"),
        max_length=200,
        unique=True,
        blank=False,
    )

    tag = models.CharField(
        verbose_name=_("publication:model_tag_verbose_name"),
        help_text=_("publication:model_tag_help_text"),
        max_length=255,
        unique=True,
        blank=False,
    )

    class Meta:
        abstract = True


class Publication(models.Model):
    """Base model for publications in the Green Economics app.
    This model serves as a base for articles, blog posts, and other types of content
    that require a slug, title, body, authors, status, and publication date.

    Attributes:
        slug (str): A unique identifier for the publication.
        title (str): The title of the publication.
        body (str): The body of the publication.
        authors (str): The authors of the publication.
        status (str): The status of the publication.
        publication_date (datetime): The date the publication was published.
        created_at (datetime): The date and time the publication was created.
        updated_at (datetime): The date and time the publication was last updated.

    Example:
        >>> publication = Publication(
        >>>     slug="my-first-article",
        >>>     title="My First Article",
        >>>     body="This is the body of my first article.",
        >>>     authors="John Doe",
        >>>     status=PublicationStatus.DRAFT,
        >>>     publication_date=None,
        >>> )
        >>> publication.save()
    """

    slug = models.SlugField(
        verbose_name=_("publication:model_slug_verbose_name"),
        help_text=_("publication:model_slug_help_text"),
        max_length=200,
        unique=True,
        blank=False,
        null=False,
    )
    title = models.CharField(
        verbose_name=_("publication:model_title_verbose_name"),
        help_text=_("publication:model_title_help_text"),
        unique=True,
        blank=False,
        null=False,
        max_length=255,
    )
    summary = models.TextField(
        verbose_name=_("publication:model_summary_verbose_name"),
        help_text=_("publication:model_summary_help_text"),
        blank=True,
        default="",
        max_length=500,
    )
    body = models.TextField(
        verbose_name=_("publication:model_body_verbose_name"),
        help_text=_("publication:model_body_help_text"),
        blank=True,
    )
    authors = models.CharField(
        verbose_name=_("publication:model_authors_verbose_name"),
        help_text=_("publication:model_authors_help_text"),
        max_length=255,
        blank=True,
        default="",
    )
    status = models.CharField(
        verbose_name=_("publication:model_status_verbose_name"),
        help_text=_("publication:model_status_help_text"),
        max_length=2,
        choices=PublicationStatus.choices,
        default=PublicationStatus.DRAFT,
    )
    publication_date = models.DateField(
        verbose_name=_("publication:model_publication_date_verbose_name"),
        help_text=_("publication:model_publication_date_help_text"),
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_("publication:model_created_at_verbose_name"),
        help_text=_("publication:model_created_at_help_text"),
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        verbose_name=_("publication:model_updated_at_verbose_name"),
        help_text=_("publication:model_updated_at_help_text"),
        auto_now=True,
    )

    class Meta:
        abstract = True
