from django.contrib import admin

from materials.models import Material

#admin.site.register(Material)

@admin.register(Material)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name',)
    search_fields = ('name', 'description')