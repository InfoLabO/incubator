from django.db import models
from django.core.files.storage import Storage, FileSystemStorage
from django.conf import settings


class Storage(models.Model):
    file = models.FileField(upload_to='files')
    date = models.DateTimeField(auto_now=True)

