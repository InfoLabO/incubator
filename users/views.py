from urllib import request

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import viewsets
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.views.decorators.http import require_POST
from django.views.generic.detail import DetailView
from django.views.generic import UpdateView
from django.urls import reverse
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import login, authenticate
from users.forms import UserCreationForm
from .serializers import UserSerializer
from .models import User
from .forms import UserForm, ChangePasswordForm, AdminChangePasswordForm
from .tokens import account_activation_token


"""def send_activate_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activez votre compte'
    email_body = render_to_string('activate.html',{
        'user':user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':generate_token.make_token(user)
    })

    email=EmailMessage(subject=email_subject,body=email_body,
                 from_email=settings.EMAIL_FROM_USER,to=[user.email])
    email.send()
"""


@require_POST
def login_view(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        next = request.GET.get("next", "/")
        next = next if next != "" else "/"
        return HttpResponseRedirect(next)
    else:
        messages.error(request, "Aucun compte correspondant à cet identifiant n'a été trouvé")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])


def show_pamela(request):
    request.user.hide_pamela = False
    request.user.save()
    return HttpResponseRedirect(reverse('profile'))


def hide_pamela(request):
    request.user.hide_pamela = True
    request.user.save()
    return HttpResponseRedirect(reverse('profile'))


def change_passwd(request):
    user = request.user
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            if user.check_password(form.cleaned_data['old_password']):
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                messages.add_message(request, messages.INFO, "Vous devez vous reconnecter pour continuer")
                return HttpResponseRedirect(reverse("login"))
            else:
                messages.add_message(request, messages.ERROR, "Le mot de passe est incorrect")
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            messages.add_message(request, messages.ERROR, "Les mots de passe ne correspondent pas")
            return HttpResponseRedirect(request.META['HTTP_REFERER'])

    context = {
        "form": ChangePasswordForm()
    }
    return render(request, "change_passwd.html", context)


def admin_change_passwd(request, id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        form = AdminChangePasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            messages.add_message(request, messages.INFO, "Le mot de passe a bien ete modifier")
            return HttpResponseRedirect("/admin")
        else:
            messages.add_message(request, messages.ERROR, "Les mots de passe ne sont pas identiques!")

    context = {
        "form": AdminChangePasswordForm(),
        "user_id": id
    }
    return render(request, "admin_change_passwd.html", context)


class UserEditView(UpdateView):
    form_class = UserForm
    template_name = 'user_form.html'

    def get_success_url(self):
        return reverse('profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user'
    slug_field = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request

        TRANSACTION_NUM = 5  # Number of transactions to be shown on the page

        # Public
        streampubtosend = self.object.actor_actions.filter(public=True)\
            .prefetch_related('target', 'actor', 'action_object')[:TRANSACTION_NUM]

        # Private
        all_private_transactions = []
        if request.user == self.object:
            transfers = list(request.user.transfertransaction_set.all().order_by("-when")[:TRANSACTION_NUM])
            topups = list(request.user.topuptransaction_set.all().order_by("-when")[:TRANSACTION_NUM])
            purchases = list(request.user.producttransaction_set.all().order_by("-when")[:TRANSACTION_NUM])
            misc = list(request.user.misctransaction_set.all().order_by("-when")[:TRANSACTION_NUM])
            # Sort all transactions and keep only the TRANSACTION_NUM most recent
            all_private_transactions = sorted(
                transfers + topups + purchases + misc, key=lambda x: x.when, reverse=True)[:TRANSACTION_NUM]

        context['stream_pub'] = streampubtosend
        context['stream_priv'] = all_private_transactions

        return context


class CurrentUserDetailView(UserDetailView):
    def get_object(self):
        return self.request.user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def RegisterView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = HttpRequest.get_host(self=request)
            email_subject = 'Activez votre compte'
            message = render_to_string('activate.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                email_subject, message, 'contact@infolabo.fr',
                [to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return redirect(reverse('login'))
    else:
        return HttpResponse("Le lien d'activation n'est pas valide !")


"""def activate_user(request,uidb64,token):

    try:
        uid=force_text(urlsafe_base64_encode(uidb64))
        user=User.objects.get(pk=uid)
    except Exception as e:
        user=None

    if user and generate_token.check_token(user,token):
        user.is_email_verified=True
        user.save()
        messages.add_message(request,messages.SUCCESS,'Email vérifié avec succès, vous pouvez maintenant vous connecté')
        return redirect(reverse('login_view'))

    return render(request,'activate_failed.html',{'user':})"""