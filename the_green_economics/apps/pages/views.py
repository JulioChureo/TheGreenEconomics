from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from the_green_economics.apps.articles.models import Article

HOME_QUERYSET = (
    Article.objects.all()
    .order_by("-created_at")[:15]
    .values(
        "id",
        "title",
        "slug",
        "publication_date",
    )
)


class HomeView(TemplateView):
    """Home view. extract the last 5 articles and news from the database"""

    template_name = "pages/home.html"

    def get_queryset(self):
        queryset = cache.get_or_set(
            "home-articles",
            HOME_QUERYSET,
            timeout=60 * 15,
        )

        if queryset is None:
            queryset = HOME_QUERYSET
            cache.set("home-articles", queryset, timeout=60 * 15)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = list(self.get_queryset())
        return context


class ContactView(View):
    template_name = "pages/publish.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # Aquí puedes procesar el formulario
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        institution = request.POST.get("institution")
        title = request.POST.get("title")
        research_area = request.POST.get("research_area")
        summary = request.POST.get("summary")
        manuscript = request.FILES.get("manuscript")

        # Ejemplo básico de manejo de archivo (solo impresión por ahora)
        if manuscript:
            print(f"Archivo recibido: {manuscript.name}")

        # Aquí normalmente guardarías los datos en la base de datos o enviarías un correo
        messages.success(request, "Tu propuesta fue enviada con éxito.")
        return redirect("publish")  # Nombre de tu urlpattern
