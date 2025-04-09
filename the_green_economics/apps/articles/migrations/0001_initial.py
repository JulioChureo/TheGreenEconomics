# Generated by Django 5.0.13 on 2025-04-09 01:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='article tag name')),
                ('slug', models.SlugField(unique=True, verbose_name='article tag slug')),
            ],
            options={
                'verbose_name': 'article tag',
                'verbose_name_plural': 'article tags',
                'indexes': [models.Index(fields=['name'], name='articles_ar_name_6b7ff8_idx'), models.Index(fields=['slug'], name='articles_ar_slug_23be95_idx')],
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='article title')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='article slug')),
                ('authors', models.CharField(blank=True, max_length=200, verbose_name='article authors')),
                ('publication_date', models.DateField(blank=True, null=True, verbose_name='article publication date')),
                ('abstract', models.TextField(verbose_name='article abstract')),
                ('body', models.TextField(verbose_name='article body')),
                ('pdf', models.FileField(upload_to='articles/pdfs/', validators=[django.core.validators.FileExtensionValidator(['pdf'])], verbose_name='archivo PDF')),
                ('status', models.CharField(choices=[('DF', 'Borrador'), ('PB', 'Publicado'), ('UR', 'En revisión')], default='DF', max_length=2, verbose_name='article status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='fecha de actualización')),
                ('tags', models.ManyToManyField(blank=True, related_name='articles', to='articles.articletag', verbose_name='etiquetas')),
            ],
            options={
                'verbose_name': 'artículo científico',
                'verbose_name_plural': 'artículos científicos',
                'ordering': ['-publication_date'],
                'indexes': [models.Index(fields=['publication_date'], name='articles_ar_publica_044c0c_idx'), models.Index(fields=['status', 'publication_date'], name='articles_ar_status_d150a8_idx'), models.Index(fields=['slug'], name='articles_ar_slug_452037_idx')],
            },
        ),
    ]
