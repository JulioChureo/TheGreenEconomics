from django.core.management.base import BaseCommand

from the_green_economics.apps.articles.tests.factories import ArticleFactory


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--article_amount",
            type=int,
            default=10,
        )

    def handle(self, *args, **options):
        article_amount = options["article_amount"]

        articles = ArticleFactory.create_batch(
            size=article_amount,
        )
        self.stdout.write(
            self.style.SUCCESS(f"{articles}"),
        )
