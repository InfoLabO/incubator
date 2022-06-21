# Generated by Django 3.2.10 on 2022-06-05 21:15

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0006_photo_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='cover',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format=None, keep_meta=True, null=True, quality=100, size=[500, 500], upload_to='gallery_pictures'),
        ),
    ]
