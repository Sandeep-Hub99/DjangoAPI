from django.contrib import admin
from .models import Article,Passenger

# Register your models here.
admin.site.register(Passenger)

@admin.register(Article)
class ArticleModel(admin.ModelAdmin):
    list_filter = ('title','description')
    list_display = ('title','description')