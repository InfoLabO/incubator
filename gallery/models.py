from django.db import models
from django.urls import reverse
from django_resized import ResizedImageField


class Album(models.Model):
    title = models.CharField(max_length=300, verbose_name='Nom')
    cover = ResizedImageField(
        size=[500, 500], crop=['middle', 'center'], quality=100, upload_to='gallery_pictures', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    short_description = models.CharField(max_length=1000, verbose_name="Description courte")

    class Meta:
        verbose_name = "Album"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('gallery_home')


class Tag(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False,unique=True)

    def __str__(self):
        return self.name


class Photo(models.Model):
    short_description = models.CharField(max_length=1000,blank=True)
    name = models.CharField(max_length=100,default="image",blank=True)
    album = models.ForeignKey(Album, verbose_name='Album', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag,blank=True)
    picture = ResizedImageField(
    size=[500, 500], crop=['middle', 'center'], quality=100, upload_to='gallery_pictures', null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('view_album',args=[self.album_id])



