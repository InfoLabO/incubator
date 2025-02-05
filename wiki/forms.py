from django.forms import ModelForm, Textarea
from .models import Article


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        exclude = ['creator', 'last_modifier']

        widgets = {
            'content': Textarea(attrs={'rows': 20}),
            'summary': Textarea(attrs={'rows': 7}),
        }

