# Generated by Django 3.2.10 on 2022-05-19 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_alter_storage_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='storage',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
