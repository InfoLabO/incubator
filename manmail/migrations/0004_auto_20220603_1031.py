# Generated by Django 3.2.10 on 2022-06-03 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manmail', '0003_auto_20220602_1545'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='destinataire',
        ),
        migrations.AlterField(
            model_name='email',
            name='content',
            field=models.TextField(blank=True, null=True, verbose_name='Contenu'),
        ),
    ]
