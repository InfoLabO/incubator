from django.contrib import admin
from .models import Album, Tag, Photo


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description')


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('short_description','picture','album')
    filter_horizontal = ('tags',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

