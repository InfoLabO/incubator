# Generated by Django 3.2.10 on 2022-06-05 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_auto_20220605_1647'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='picture',
        ),
    ]
