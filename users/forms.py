from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from django import forms
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', ]


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("Mot de passe différent."),
    }
    password1 = forms.CharField(
        label=_("Mot de passe"),
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label=_("Confirmer mot de passe"),
        widget=forms.PasswordInput,
    )
    first_name = forms.CharField(
        label=_("Prénom"),
    )

    last_name = forms.CharField(
        label=_("Nom"),
    )

    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ("username","first_name", "last_name", "email", "password1", "password2")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def auth_user(self):
        user = authenticate(
            username=self.cleaned_data.get("username"),
            password=self.cleaned_data.get("password1"),
        )

        return user


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label=_("Ancien mot de passe"),
        widget=forms.PasswordInput
    )
    new_password = forms.CharField(
        label=_("Nouveau mot de passe"),
        widget=forms.PasswordInput
    )
    new_password2 = forms.CharField(
        label=_("Confirmer nouveau mot de passe"),
        widget=forms.PasswordInput,
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("new_password2")

        if password != confirm_password:
            self.add_error('new_password', "Les mots de passe ne sont pas identiques!")


class AdminChangePasswordForm(forms.Form):

    new_password = forms.CharField(
        label=_("Nouveau mot de passe"),
        widget=forms.PasswordInput
    )
    new_password2 = forms.CharField(
        label=_("Confirmer nouveau mot de passe"),
        widget=forms.PasswordInput,
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("new_password2")

        if password != confirm_password:
            self.add_error('new_password', "Les mots de passe ne sont pas identiques!")
