# Generated by Django 3.2.10 on 2022-06-02 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20220530_1518'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='avatar',
        ),
        migrations.AddField(
            model_name='user',
            name='newsletter',
            field=models.BooleanField(default=True, verbose_name='abonné à la newsletter'),
        ),
    ]
