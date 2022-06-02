from manmail.models import Email

from django import forms


class ContactForm(forms.Form):
    À = forms.EmailField(required=True)
    Objet = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea)


"""class CommentForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['', 'project', 'author']"""