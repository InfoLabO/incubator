from datetime import datetime

from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.contrib import admin
from django.contrib import auth
from django.urls import reverse
from django.utils.html import format_html

from .models import User
from space.models import MacAdress


class MacAdressInline(admin.TabularInline):
    model = MacAdress
    extra = 1


@admin.register(User)
class UserAdmin(UserAdmin):

    def change_password(self, user):
        url = reverse("admin_change_passwd", args=(user.id,))
        return format_html(f"<a href='{url}'>Changer le mot de passe</a>")
    change_password.allow_tags = True

    list_display = ('username', 'email', 'is_superuser', 'created', 'newsletter', 'is_active')
    list_filter = ('is_superuser', 'created', 'last_login', 'username',)
    search_fields = ('username', 'email', 'first_name', 'last_name')

    inlines = (MacAdressInline,)
    filter_horizontal = ('user_permissions', )
    readonly_fields = ('change_password', )

    fieldsets = (
        (None, {
            'fields': (
                ('username', 'email'),
                ('first_name', 'last_name'),
                ('hide_pamela', 'newsletter',),

            )
        }),
        (None, {
            'fields': ('change_password', 'last_login')
        }),
        ('Permissions', {
            'classes': ('collapse',),
            'fields': ('is_superuser', 'user_permissions')
        }),
    )

    add_form = auth.forms.UserCreationForm
    form = auth.forms.UserChangeForm
