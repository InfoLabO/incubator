from django.conf import settings
from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords
# from datetime import datetime
# from projects.models import Project

User = settings.AUTH_USER_MODEL

CATEGORY = (
    ("p", "Projets"),
    ("m", "Matériels"),
    ("e", "Expérience & conseils"),
    ("d", "Divers"),
    ("h", "Hackerspace")
)


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Nom")
    creator = models.ForeignKey(User, related_name="writted_article", verbose_name="Auteur", on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    last_modifier = models.CharField(max_length=50, default="")
    last_modified = models.DateTimeField(auto_now=True)
    content = models.TextField(verbose_name="Contenu", blank=True)
    history = HistoricalRecords()
    commit = models.TextField(verbose_name="commit", blank=True)
    category = models.CharField(max_length=1, choices=CATEGORY)
    hidden = models.BooleanField(default=False, verbose_name="Caché")
    is_feeding_home_page = models.BooleanField(default=False, verbose_name="Visible sur la page d'accueil du site")

    class Meta:
        verbose_name = "Article"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_article', args=[self.pk])


class ProjectLinkedArticle(Article):
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
