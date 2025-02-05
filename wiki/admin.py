from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'hidden', 'category','is_feeding_home_page', 'creator', 'created', 'last_modifier', 'last_modified')
    search_fields = ('title', 'creator__username', 'summary', 'id')
    list_filter = ('category', 'hidden','is_feeding_home_page')
