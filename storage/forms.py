from django import forms

from storage.models import Storage


class StorageForm(forms.ModelForm):
    class Meta:
        model = Storage
        fields = ('file', )

