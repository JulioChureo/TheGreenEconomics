from django.contrib import admin

from the_green_economics.apps.news.models import News
from the_green_economics.apps.news.models import NewsTag

admin.site.register(News)
admin.site.register(NewsTag)
