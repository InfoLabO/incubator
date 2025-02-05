# Generated by Django 3.2.10 on 2022-06-02 13:45

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('manmail', '0002_email_approvers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='approvers',
        ),
        migrations.AddField(
            model_name='email',
            name='destinataire',
            field=models.ManyToManyField(blank=True, related_name='dest', to=settings.AUTH_USER_MODEL, verbose_name='destinataire'),
        ),
        migrations.AlterField(
            model_name='email',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Contenu'),
        ),
    ]
