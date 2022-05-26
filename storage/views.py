import os

from actstream import action
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView

from storage.forms import StorageForm
from storage.models import Storage


def StorageHomeView(request):
    files = os.listdir('media/files')
    if request.method == 'POST':
        form = StorageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/storage/')
    else:
        form = StorageForm()
        return render(request, 'storage_home.html', {'form': form, 'files':files })
