from django.db import models

# Create your models here.
from django.urls import reverse


class Women(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL-slug")
    content = models.TextField(blank=True, verbose_name="Текст статті")
    photo = models.ImageField(upload_to="photos/%Y/%m/", verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name="На сайті")
    category = models.ForeignKey("Category", on_delete=models.PROTECT, verbose_name="Категорії")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('get_post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = "Відомі жінки"
        verbose_name_plural = "Відомі жінки"
        ordering = ["-time_create", "title"]


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Назва")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL-slug")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ["name"]
