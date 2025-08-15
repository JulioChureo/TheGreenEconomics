from the_green_economics.apps.articles.models import Article
from the_green_economics.apps.utils.models import PublicationStatus

HOME_QUERYSET = (
    Article.objects.filter(status=PublicationStatus.PUBLISHED)
    .order_by("-created_at")[:15]
    .values("id", "title", "slug", "publication_date", "summary")
)
