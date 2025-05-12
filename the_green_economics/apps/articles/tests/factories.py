from factory import Faker
from factory.django import DjangoModelFactory

from the_green_economics.apps.articles.models import Article


class ArticleFactory(DjangoModelFactory[Article]):
    class Meta:
        model = Article
        django_get_or_create = ["title"]

    title = Faker("sentence", nb_words=6)
    authors = Faker("name")
    publication_date = Faker("date")
    status = "PB"
    abstract = Faker("text", max_nb_chars=100)
    body = Faker("text", max_nb_chars=500)

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        """Save again the instance if creating and at least one hook ran."""
        if create and results and not cls._meta.skip_postgeneration_save:
            # Some post-generation hooks ran, and may have modified us.
            instance.save()
