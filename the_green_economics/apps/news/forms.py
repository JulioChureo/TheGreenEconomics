from django import forms
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from the_green_economics.apps.utils.models import PublicationStatus

from .models import News
from .models import NewsTag

MAX_LENGTH_EXCERPT = 300


class NewsForm(forms.ModelForm):
    publication_date = forms.DateTimeField(
        label=_("news:form_publication_date_label"),
        help_text=_("news:form_publication_date_help_text"),
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        input_formats=["%Y-%m-%dT%H:%M"],
    )

    tags = forms.ModelMultipleChoiceField(
        label=_("news:form_tags_label"),
        help_text=_("news:form_tags_help_text"),
        queryset=NewsTag.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "select2"}),
        required=False,
    )

    class Meta:
        model = News
        fields = [
            "title",
            "body",
            "excerpt",
            "featured_image",
            "publication_date",
            "status",
            "tags",
        ]
        labels = {
            "title": _("news:form_title_label"),
            "body": _("news:form_body_label"),
            "excerpt": _("news:form_excerpt_label"),
            "featured_image": _("news:form_featured_image_label"),
            "status": _("news:form_status_label"),
        }
        widgets = {
            "status": forms.Select(choices=PublicationStatus.choices),
            "excerpt": forms.Textarea(attrs={"rows": 3}),
            "body": forms.Textarea(attrs={"rows": 15, "class": "rich-editor"}),
        }
        help_texts = {
            "excerpt": _("news:form_excerpt_help_text"),
            "publication_date": _("news:form_publication_date_help_text"),
            "status": _("news:form_status_help_text"),
            "tags": _("news:form_tags_help_text"),
            "title": _("news:form_title_help_text"),
            "body": _("news:form_body_help_text"),
            "featured_image": _("news:form_featured_image_help_text"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields["slug"] = forms.SlugField(
                required=False,
                widget=forms.HiddenInput(),
                help_text=_("news:form_slug_help_text"),
            )

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        title = self.cleaned_data.get("title")
        instance = self.instance

        if not slug and title:
            base_slug = slugify(title)
            unique_slug = base_slug
            counter = 1
            while (
                News.objects.filter(slug=unique_slug).exclude(pk=instance.pk).exists()
            ):
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            return unique_slug

        if slug:
            existing = News.objects.filter(slug=slug).exclude(pk=instance.pk)
            if existing.exists():
                raise forms.ValidationError(_("Este identificador URL ya está en uso"))
            return slug

        return slug

    def clean_excerpt(self):
        excerpt = self.cleaned_data.get("excerpt")
        if len(excerpt) > MAX_LENGTH_EXCERPT:
            raise forms.ValidationError(
                _("El extracto no puede exceder los 300 caracteres"),
            )
        return excerpt

    def save(self, commit=True):
        instance = super().save(commit=False)

        if not instance.pk and not instance.slug:
            instance.slug = self.cleaned_data["slug"]

        if commit:
            instance.save()
            self.save_m2m()

        return instance


class DeleteNewsForm(forms.ModelForm):
    confirmation = forms.BooleanField(
        label=_("news:form_confirmation_label"),
        help_text=_("news:form_confirmation_help_text"),
        required=True,
        initial=False,
    )

    class Meta:
        model = News
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["confirmation"].widget.attrs.update(
            {"class": "confirmation-checkbox"}
        )

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("confirmation"):
            raise forms.ValidationError(_("news:form_confirmation_error"))
        return cleaned_data

    def save(self, commit=True):
        if commit:
            self.instance.delete()
        return self.instance


class NewsTagForm(forms.ModelForm):
    class Meta:
        model = NewsTag
        fields = ["tag"]
        labels = {"tag": _("news_tag:form_name_label")}
        help_texts = {"tag": _("news_tag:form_name_help_text")}

    def clean_name(self):
        name = self.cleaned_data["tag"]
        if NewsTag.objects.filter(name__iexact=name).exists():
            if not self.instance or self.instance.name != name:
                raise forms.ValidationError(_("Esta etiqueta ya existe"))
        return name

    def save(self, commit=True):  # noqa: FBT002
        instance = super().save(commit=False)
        instance.slug = slugify(instance.name)

        # Garantizar slug único
        original_slug = instance.slug
        counter = 1
        while NewsTag.objects.filter(slug=instance.slug).exists():
            instance.slug = f"{original_slug}-{counter}"
            counter += 1

        if commit:
            instance.save()
        return instance


class DeleteNewsTagForm(forms.ModelForm):
    class Meta:
        model = NewsTag
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.clear()
