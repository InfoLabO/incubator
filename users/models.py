import hashlib
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.urls import reverse
from django.core.exceptions import ValidationError
# Create your models here.
#    User :
#    Des users ont des skills/badges
#    Les badges ne peuvent être donnés que par quelqu'un qui l'a déjà (genre des teachers)
#    un badge pourrait être "utilisateur de la reprap" et "certigfierait" que le user sait utiliser la machine
#    Des users appartiennent à un groupe (anon, registered, membres cotisants, "bureau")
#    Système d'emprunt (optionnel)


def insensitive_unique_username(username):
    # Ceci est un test en prod, pardonnez mon âme.
    # Bisous, c4.
    user = User.objects.filter(username__iexact=username).first()
    if user:
        if user.username == username:
            pass  # We already have database validation for this case
        else:
            raise ValidationError("A user named %s already exists." % username)


class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, last_login=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, is_superuser=True, **extra_fields)

    def get_by_natural_key(self, username):
        # makes user matching case insensitive
        return self.get(username__iexact=username)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'Utilisateur'
        ordering = ['username']

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()

    username = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="nom d'utilisateur",
        validators=[insensitive_unique_username]
    )
    email = models.EmailField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=127, blank=True)
    last_name = models.CharField(max_length=127, blank=True)
    hide_pamela = models.BooleanField(default=False, verbose_name='caché sur pamela')
    is_active = models.BooleanField(default=True, verbose_name='Utilisateur actif')
    newsletter = models.BooleanField(default=True, verbose_name='abonné à la newsletter')
    # , widget=forms.Textarea(attrs={'placeholder': 'Ajouter une description', 'style':'resize:none;'}))

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def gravatar(self):
        mail = self.email.lower().encode('utf8')
        gravatar_url = "//www.gravatar.com/avatar/" + hashlib.md5(mail).hexdigest() + "?d=wavatar"

        return gravatar_url

    def get_absolute_url(self):
        return reverse('user_profile', args=[self.username])


class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "Membre du hackerspace durant l'année {}".format(self.asbl_year)

