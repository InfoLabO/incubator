from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone
from actstream import action
from bootstrap_modal_forms.generic import BSModalCreateView
from django.forms import ModelChoiceField


from .forms import AlbumForm, PhotoForm, TagForm, PhotoAddForm, TagClaForm
from .models import Album
from .models import Photo
from .models import Tag

def gallery_home(request):
    return render(request, "gallery_home.html", {
        'albums': Album.objects.all(),
        'form': TagClaForm
    })
def photo_by_tag(request):
    if request.method == 'POST':
        tagList = request.POST.getlist('name')
        photos = Photo.objects.filter(tags__in=tagList)
        photos_dict = {
            'photos':photos,
            'form':TagClaForm(initial={'name':tagList})
        }
        return render(request, 'photo_by_tag.html',photos_dict)

def delete_photo(request,album_id,photo_id):
    photo = Photo.objects.get(pk=photo_id)
    photo.delete()

    return redirect(reverse('view_album', kwargs={'pk': album_id}))

def delete_album(request,album_id):
    album = Album.objects.get(pk=album_id)
    album.delete()

    return render(request, "gallery_home.html", {
        'albums': Album.objects.all(),
        'form': TagClaForm
    })

class AlbumEditView(UpdateView):
    form_class = AlbumForm
    model = Album
    template_name = 'add_album.html'

    def form_valid(self, form):
        ret = super(AlbumEditView, self).form_valid(form)
        action.send(self.request.user, verb='a édité', action_object=self.object)

        return ret

class TagAddView(BSModalCreateView):
    form_class = TagForm
    model = Tag
    template_name = 'add_tag.html'
    success_message = 'Tags mises à jour ! vous pouvez désormais l\'ajouter à la photo'

    def get_success_url(self):
        previous_url = self.request.META.get('HTTP_REFERER')
        return previous_url

class PhotoEditView(UpdateView):
    form_class = PhotoForm
    model = Photo
    template_name = 'update_photo.html'

    def form_valid(self, form):
        ret = super(PhotoEditView, self).form_valid(form)
        action.send(self.request.user, verb='a édité', action_object=self.object)

        return ret

    def get_context_data(self, **kwargs):
        context = super(PhotoEditView, self).get_context_data(**kwargs)
        context['photos'] = Photo.objects.filter(name=self.object)
        return context

class PhotoAddView(CreateView):
    form_class = PhotoAddForm
    model = Photo
    template_name = 'add_photo.html'

    def form_valid(self, form):
        previous_url = (self.request.META.get('HTTP_REFERER')).rsplit('/', 3)[-3]
        album=Album.objects.get(pk=previous_url)
        form.instance.album = album
        ret = super(PhotoAddView, self).form_valid(form)
        action.send(self.request.user, verb='a ajouté', action_object=self.object)

        return ret

    def get_context_data(self, **kwargs):
        context = super(PhotoAddView, self).get_context_data(**kwargs)
        context['photos'] = Photo.objects.filter(name=self.object)
        return context


class AlbumDetailView(DetailView):
    model = Album
    template_name = 'album_detail.html'
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super(AlbumDetailView, self).get_context_data(**kwargs)
        context['photos'] = Photo.objects.filter(album = self.object)
        context['tags'] = Tag.objects.filter()
        return context



class AlbumAddView(CreateView):
    form_class = AlbumForm
    model = Album
    template_name = 'add_album.html'

    def form_valid(self, form):
        ret = super(AlbumAddView, self).form_valid(form)
        action.send(self.request.user, verb='a créé', action_object=self.object)

        return ret