from django.contrib import admin
from .models import AdvUser, Product, Category, ThingCategory
# Register your models here.

admin.site.register(AdvUser)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ThingCategory)