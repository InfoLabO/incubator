from django.contrib import admin

from storage.models import Storage


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('file', 'date')
    list_filter = ('file', 'date',)
    search_fields = ('file',)
