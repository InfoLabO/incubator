from django.shortcuts import render
from rest_framework import viewsets
from django.views.generic.detail import DetailView
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from actstream import action

from .serializers import ArticleSerializer
from .models import Article
from .forms import ArticleForm


def wiki_home(request):
    articles = Article.objects.all().filter(hidden=False)

    return render(request, "wiki_home.html", {
        'project': articles.filter(category="p"),
        'materials': articles.filter(category="m"),
        'experiences': articles.filter(category="e"),
        'miscellaneous': articles.filter(category="d"),
        'hackerspace': articles.filter(category="h"),
    })


class ArticleAddView(LoginRequiredMixin, CreateView):
    form_class = ArticleForm
    template_name = 'add_article.html'
    login_url = '/auth/login/'
    redirect_field_name = 'redirect_to'

    def get_form(self, *args, **kwargs):
        form = super().get_form(self.form_class)
        if not self.request.user.is_superuser:
            form.fields.pop('is_feeding_home_page')
        return form

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.last_modifier = self.request.user.get_username()
        ret = super(ArticleAddView, self).form_valid(form)
        action.send(self.request.user, verb='a créé', action_object=self.object)

        return ret


class ArticleEditView(LoginRequiredMixin, UpdateView):
    form_class = ArticleForm
    model = Article
    template_name = 'add_article.html'
    login_url = '/auth/login/'
    redirect_field_name = 'redirect_to'

    def get_form(self, *args, **kwargs):
        form = super().get_form(self.form_class)
        if not self.request.user.is_superuser:
            form.fields.pop('is_feeding_home_page')
        return form

    def form_valid(self, form):
        form.instance.last_modifier = self.request.user.get_username()
        form.instance.last_modified = timezone.now()
        ret = super(ArticleEditView, self).form_valid(form)
        action.send(self.request.user, verb='a édité', action_object=self.object)

        return ret


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'


class ArticleOldDetailView(DetailView):
    model = Article.history.model
    template_name = 'article_old_detail.html'
    context_object_name = 'article'


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
