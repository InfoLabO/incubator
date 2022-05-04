from django.db import models
from django_resized import ResizedImageField


class Material(models.Model):

    name = models.CharField(max_length=40)
    description = models.TextField()
    picture = ResizedImageField(
        size=[500, 500], crop=['middle', 'center'], quality=100, upload_to='materials_pictures', null=True, blank=True)
