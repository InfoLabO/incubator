from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.conf import settings


class Email(models.Model):

    subject = models.CharField(max_length=511, verbose_name="Sujet")
    content = models.TextField(null=True, blank=True, verbose_name="Contenu")
    sent = models.BooleanField(default=False, verbose_name="Envoyé")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
