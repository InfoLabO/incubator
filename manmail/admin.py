from django.contrib import admin
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings

from incubator.settings import EMAIL_HOST_USER
from .models import Email
from users.models import User


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sent', 'created', 'modified', )
    list_filter = ('sent', 'created', 'modified')
    search_fields = ('subject', 'content', )
    readonly_fields = ('sent', )
    actions = ["send_email", "send_test_email", ]

    def send_email(self, request, queryset):
        if not queryset.count() == 1:
            self.message_user(request, message="Vous ne devez séléctionner qu'un email à envoyer", level=messages.ERROR)
            return

        email = queryset.first()

        if email.sent:
            self.message_user(request, message="Cet email a déjà été envoyé", level=messages.ERROR)
            return

        recipients = [u.email for u in User.objects.filter(newsletter=True)]
        send_mail(
            email.subject,
            email.content,
            EMAIL_HOST_USER,
            recipients,
            fail_silently=False,
        )
        email.sent = True
        email.save()
        self.message_user(request, "L'email a été énvoyé.")

    send_email.short_description = "Envoyer cet email A TOUT LE MONDE"

    def send_test_email(self, request, queryset):
        if not queryset.count() == 1:
            self.message_user(request, message="Vous ne devez séléctionner qu'un email à envoyer", level=messages.ERROR)
            return

        email = queryset.first()

        if email.sent:
            self.message_user(request, message="Cet email a déjà été envoyé", level=messages.ERROR)
            return

        message = EmailMultiAlternatives(
            subject=email.subject,
            body = email.content,
            from_email = EMAIL_HOST_USER,
            to=["soumaha745@gmail.com"],
            bcc=["soumaha745@gmail.com"],
        )

        message.send()
        self.message_user(request, "L'email a été énvoyé à votre adresse")
    send_test_email.short_description = "Envoyer cet email A MOI UNIQUEMENT"

