from django.contrib import admin

from the_green_economics.apps.articles.models import Article
from the_green_economics.apps.articles.models import ArticleTag


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "publication_date", "status")
    list_filter = ("status",)
    search_fields = ("title", "body", "authors")
    ordering = ("-publication_date",)


class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    ordering = ("name",)


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleTag, ArticleTagAdmin)
