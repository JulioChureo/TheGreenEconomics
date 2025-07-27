from django import forms
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from the_green_economics.apps.articles.models import Article
from the_green_economics.apps.articles.models import ArticleTag
from the_green_economics.apps.utils.models import PublicationStatus


class ArticleForm(forms.ModelForm):
    publication_date = forms.DateField(
        label=_("article:form_publication_date_label"),
        help_text=_("article:form_publication_date_help_text"),
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = Article
        fields = [
            "title",
            "authors",
            "publication_date",
            "summary",
            "pdf",
            "status",
            "doi",
            "issn",
        ]
        labels = {
            "title": _("article:form_title_label"),
            "authors": _("article:form_authors_label"),
            "publication_date": _("article:form_publication_date_label"),
            "summary": _("article:form_summary_label"),
            "pdf": _("article:form_pdf_label"),
            "status": _("article:form_status_label"),
            "doi": _("article:form_doi_label"),
            "issn": _("article:form_issn_label"),
        }
        help_texts = {
            "pdf": _("article:form_pdf_help_text"),
            "status": _("article:form_status_help_text"),
            "title": _("article:form_title_help_text"),
            "authors": _("article:form_authors_help_text"),
            "publication_date": _("article:form_publication_date_help_text"),
            "summary": _("article:form_summary_help_text"),
            "doi": _("article:form_doi_help_text"),
            "issn": _("article:form_issn_help_text"),
        }
        widgets = {
            "status": forms.Select(choices=PublicationStatus.choices),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["tags"].queryset = ArticleTag.objects.all()

        # Generar slug automáticamente si es nuevo artículo
        if not self.instance.pk:
            self.fields["slug"] = forms.SlugField(
                required=False,
                widget=forms.HiddenInput(),
            )

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        title = self.cleaned_data.get("title")

        if not slug and title:
            slug = slugify(title)
            unique_slug = slug
            counter = 1
            while Article.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{slug}-{counter}"
                counter += 1
            return unique_slug
        return slug


class ArticleRestoreForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["status"]
        labels = {"status": _("article:form_status")}
        help_texts = {"status": _("article:form_status_help_text")}
        widgets = {
            "status": forms.Select(choices=PublicationStatus.choices),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DeleteArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = []  # No necesita campos

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.clear()


class ArticleTagForm(forms.ModelForm):
    class Meta:
        model = ArticleTag
        fields = ["tag"]
        labels = {"tag": _("nombre de la etiqueta")}
        help_texts = {"tag": _("Nombre único para la etiqueta")}

    def clean_name(self):
        name = self.cleaned_data["tag"]
        if ArticleTag.objects.filter(name__iexact=name).exists():
            if not self.instance or self.instance.name != name:
                raise forms.ValidationError(_("Esta etiqueta ya existe"))
        return name

    def save(self, commit=True):  # noqa: FBT002
        instance = super().save(commit=False)
        instance.slug = slugify(instance.name)

        # Garantizar slug único
        original_slug = instance.slug
        counter = 1
        while ArticleTag.objects.filter(slug=instance.slug).exists():
            instance.slug = f"{original_slug}-{counter}"
            counter += 1

        if commit:
            instance.save()
        return instance


class DeleteArticleTagForm(forms.ModelForm):
    class Meta:
        model = ArticleTag
        fields = []  # No necesita campos

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.clear()
