from django.contrib import admin
from .models import ArticleModels
# Register your models here.


@admin.register(ArticleModels)
class ArticleModels(admin.ModelAdmin):
    pass

