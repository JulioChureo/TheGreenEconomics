from django.db import models
from django.utils.text import slugify

class JournalEntry(models.Model):
    titulo = models.CharField(max_length=100)
    content = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True, null=False)
    estado = models.BooleanField(default=True) 

    def save(self, *args, **kwargs):
        # Generar slug automáticamente si no existe
        if not self.slug:
            self.slug = slugify(self.titulo)
            # Asegurarse de que el slug sea único
            original_slug = self.slug
            counter = 1
            while JournalEntry.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo