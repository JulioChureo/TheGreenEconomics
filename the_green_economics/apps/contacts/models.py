from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class ResearchProposalTypes(models.TextChoices):
    """Enumeration for research proposal types."""

    ECONOMIA_CIRCULAR = "bs", _("Economía Circular")
    ENERGIA_RENOVABLE = "er", _("Energía Renovable")
    DESARROLLO_SOSTENIBLE = "ds", _("Desarrollo Sostenible")
    POLITICA_AMBIENTAL = "pa", _("Política Ambiental")
    FINANZAS_VERDES = "fv", _("Finanzas Verdes")
    OTROS = "ot", _("Otros")


class ResearchProposal(models.Model):
    first_name = models.CharField(
        max_length=100,
        verbose_name="research_proposal:first_name_verbose_name",
        help_text="research_proposal:first_name_help_text",
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name="research_proposal:last_name_verbose_name",
        help_text="research_proposal:last_name_help_text",
    )
    email = models.EmailField(
        max_length=254,
        verbose_name="research_proposal:email_verbose_name",
        help_text="research_proposal:email_help_text",
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="research_proposal:phone_verbose_name",
        help_text="research_proposal:phone_help_text",
    )
    institution = models.CharField(
        max_length=200,
        verbose_name="research_proposal:institution_verbose_name",
        help_text="research_proposal:institution_help_text",
    )
    title = models.CharField(
        max_length=255,
        verbose_name="research_proposal:title_verbose_name",
        help_text="research_proposal:title_help_text",
    )
    research_area = models.CharField(
        max_length=50,
        choices=ResearchProposalTypes.choices,
        verbose_name="research_proposal:research_area_verbose_name",
        help_text="research_proposal:research_area_help_text",
    )
    abstract = models.TextField(
        verbose_name="research_proposal:abstract_verbose_name",
        help_text="research_proposal:abstract_help_text",
    )
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="research_proposal:creation_date_verbose_name",
        help_text="research_proposal:creation_date_help_text",
    )

    class Meta:
        verbose_name = _("research_proposal:verbose_name")
        verbose_name_plural = _("research_proposal:verbose_name_plural")
        get_latest_by = "creation_date"
        ordering = ["-creation_date"]
        indexes = [
            models.Index(fields=["email", "creation_date"]),
        ]
        unique_together = [
            ("email", "creation_date"),
            ("first_name", "last_name", "institution"),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.title}"

    def get_absolute_url(self):
        return reverse("dashboards:research-proposal-detail", kwargs={"pk": self.pk})

    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            "id": self.pk,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "institution": self.institution,
            "title": self.title,
            "research_area": self.research_area,
            "abstract": self.abstract,
            "creation_date": self.creation_date.isoformat(),
        }
