from django.contrib import admin

from space.models import MacAdress, SpaceStatus, PrivateAPIKey


@admin.register(MacAdress)
class MacAdressAdmin(admin.ModelAdmin):
    list_display = ('adress', 'holder', 'machine_name')
    search_fields = ('adress', 'holder')


@admin.register(SpaceStatus)
class SpaceStatusAdmin(admin.ModelAdmin):
    list_display = ('time', 'is_open')
    list_filter = ('time', 'is_open')



@admin.register(PrivateAPIKey)
class PrivateAPIKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'active', 'key')
    list_filter = ('user', 'active')
