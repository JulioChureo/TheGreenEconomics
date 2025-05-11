import django_filters

from the_green_economics.apps.articles.models import Article
from the_green_economics.apps.articles.models import ArticleTag


class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = ["publication_date", "title"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["publication_date"].field.widget.attrs["class"] = "w-full"
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
