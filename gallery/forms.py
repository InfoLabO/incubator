from django import forms
from django.forms import ModelChoiceField, ModelMultipleChoiceField

from .models import Album
from .models import Photo
from .models import Tag
from bootstrap_modal_forms.forms import BSModalModelForm


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'short_description', 'cover']

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ['album', 'created','picture']

class PhotoAddForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['name','short_description','tags','picture']
        exclude = ['album', 'created']

class TagForm(BSModalModelForm):
    class Meta:
        model = Tag
        fields = ['name',]


class TagClaForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['name', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name']= ModelMultipleChoiceField(queryset=Tag.objects.all())
        self.fields['name'].label=''



