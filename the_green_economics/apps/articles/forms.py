from django import forms
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .models import Article
from .models import ArticleTag


class ArticleForm(forms.ModelForm):
    publication_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        label=_("fecha de publicación"),
    )

    class Meta:
        model = Article
        fields = [
            "title",
            "authors",
            "publication_date",
            "abstract",
            "body",
            "pdf",
            #"tags",
            "status",
        ]
        labels = {
            "title": _("título"),
            "abstract": _("resumen"),
            "summary": _("sumario ejecutivo"),
            "body": _("cuerpo del artículo"),
            "pdf": _("archivo PDF"),
            #"tags": _("etiquetas"),
            "status": _("estado"),
        }
        help_texts = {
            "pdf": _("Solo se permiten archivos en formato PDF"),
        }
        widgets = {
            "status": forms.Select(choices=Article.Status.choices),
            #"tags": forms.SelectMultiple(attrs={"class": "select2"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields["tags"].queryset = ArticleTag.objects.all()

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
        fields = ["name"]
        labels = {"name": _("nombre de la etiqueta")}
        help_texts = {"name": _("Nombre único para la etiqueta")}

    def clean_name(self):
        name = self.cleaned_data["name"]
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
