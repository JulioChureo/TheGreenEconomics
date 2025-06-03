from functools import cached_property

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.cache import cache
from django.db.models import QuerySet
from django.http import FileResponse
from django.template.response import SimpleTemplateResponse
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView
from django.views.generic import ListView

CACHE_ERROR_MESSAGE = "Cache timeout exceeded"
CACHE_KEY_ERROR_MESSAGE = "Cache key not set"
CACHE_TIMEOUT_ERROR_MESSAGE = "Cache timeout not set"
FILTERSET_ERROR_MESSAGE = "Filterset class not set"
CACHE_KEY_ERROR_MESSAGE = "Cache key not set"


class PaginatedFilteredListView(ListView):
    filterset_class = None
    paginate_by = 10

    @cached_property
    def get_filterset_class(self):
        if not hasattr(self, "filterset_class") or self.filterset_class is None:
            raise AttributeError(FILTERSET_ERROR_MESSAGE)
        return self.filterset_class

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.get_filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filterset
        return context


class CacheQuerysetMixin:
    cache_timeout: int = 60
    cache_key: str = None

    def get_cache_prefix(self) -> str:
        if not hasattr(self, "cache_key") or self.cache_key is None:
            raise AttributeError(CACHE_ERROR_MESSAGE)
        raise NotImplementedError

    def get_cache_timeout(self):
        if not hasattr(self, "cache_timeout"):
            raise AttributeError(CACHE_TIMEOUT_ERROR_MESSAGE)
        return self.cache_timeout

    def get_queryset(self):
        queryset: QuerySet = cache.get_or_set(
            self.get_cache_prefix(),
            self.get_queryset(),
            self.get_cache_timeout(),
        )
        return queryset


class CachePageMixin:
    """CachePageMixin class.

    Attributes:
        cache_timeout (int): The cache timeout in seconds.

    Example:
        >>> class MyView(CachePageMixin, View):
        ...     cache_timeout = 60

    Raises:
        AttributeError: If the cache_timeout attribute is not set.
    """

    cache_timeout = 60

    @cached_property
    def get_cache_timeout(self):
        if not hasattr(self, "cache_timeout"):
            raise AttributeError(CACHE_ERROR_MESSAGE)
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        return cache_page(self.get_cache_timeout)(
            super(CachePageMixin, self).dispatch,
        )(
            *args,
            **kwargs,
        )


class AdminUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin to restrict access to admin users only.
    Inherits from LoginRequiredMixin and UserPassesTestMixin.
    """

    login_url = "users:login"
    redirect_field_name = "next"
    raise_exception = False
    permission_denied_message = "You do not have permission to access this page."

    def test_func(self):
        if not self.request.user:
            return False
        return self.request.user.is_staff or self.request.user.is_superuser


FILE_RESPONSE_ERROR_MESSAGE = "File response error: file not found or not set"
FILE_ATTRIBUTE_ERROR_MESSAGE = "File attribute not set"


class DetailedFileDownloadView(DetailView):
    file = None

    def get_file(self):
        if not hasattr(self, "file") or self.file is None:
            raise AttributeError(FILE_ATTRIBUTE_ERROR_MESSAGE)
        return self.file

    def get(self, request, *args, **kwargs):
        file = self.get_file()
        if not file:
            return SimpleTemplateResponse(
                template="404.html",
                status=404,
            )
        response: FileResponse = FileResponse(
            as_attachment=True,
            filename=file,
        )
        response["Content-Disposition"] = "attachment; filename=" + file.name
        response["X-Accel-Redirect"] = file
        return response
