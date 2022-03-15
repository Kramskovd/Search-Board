from django.db import models
from django.contrib.auth.models import AbstractUser
from sebo.addfiles.timestamppath import get_timestamp_path
# Create your models here.


class AdvUser(AbstractUser):
    date_joined = None
    is_activated = models.BooleanField(default=False, db_index=True, verbose_name='Прошел активацию?')
    number = models.PositiveIntegerField(default=False)

    class Meta(AbstractUser.Meta):
        pass


class Category(models.Model):
    name_category = models.CharField(max_length=20)

    def __str__(self):
        return self.name_category

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'
        ordering = ['name_category']


class ThingCategory(models.Model):
    name_thing = models.CharField(max_length=20, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.name_thing

    class Meta:
        verbose_name_plural = 'Разновидности'
        verbose_name = 'Название'
        ordering = ['name_thing']


class Product(models.Model):
    name_product = models.CharField(verbose_name="Название", max_length=45)
    description = models.TextField(verbose_name="Описание", max_length=500)
    price = models.PositiveIntegerField(verbose_name="Цена(руб)")
    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE)
    date_published = models.DateField(auto_now=True)
    image = models.ImageField(verbose_name='Изображение', upload_to=get_timestamp_path)
    thing_category = models.ForeignKey(ThingCategory,verbose_name="Категория", on_delete=models.CASCADE)

    def __str__(self):
        return self.name_product

    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'
        ordering = ['date_published', 'name_product']


