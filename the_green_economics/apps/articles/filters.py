import django_filters

from the_green_economics.apps.articles.models import Article
from the_green_economics.apps.articles.models import ArticleTag


class ArticleFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name="title",
        lookup_expr="icontains",
        label="Título",
    )

    class Meta:
        model = Article
        fields = ["title"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["title"].field.widget.attrs["placeholder"] = kwargs.get(
            "title_placeholder",
            "Buscar por título",
        )
        self.filters["title"].field.widget.attrs["class"] = "w-full"


class ArticleTagFilter(django_filters.FilterSet):
    class Meta:
        model = ArticleTag
        fields = ["name", "slug"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["name"].field.widget.attrs["class"] = "w-full"
        self.filters["slug"].field.widget.attrs["class"] = "w-full"
        self.filters["name"].field.widget.attrs["placeholder"] = "Nombre de la etiqueta"
        self.filters["slug"].field.widget.attrs["placeholder"] = "Slug de la etiqueta"
        self.filters["name"].field.widget.attrs["autocomplete"] = "off"
