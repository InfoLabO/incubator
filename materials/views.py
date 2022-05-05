from audioop import reverse

from django.shortcuts import render
from django.views.generic.detail import DetailView

from materials.models import Material


def materials_home(request):
    materials = Material.objects.all()
    return render(request, "materials_home.html", {
        "materials": materials,
    })


class MaterialDetailView(DetailView):
    model = Material
    template_name = 'project_detail.html'
    context_object_name = 'project'

    def get_success_url(self):
        return reverse('view_project', kwargs={'pk': self.object.id})

    """def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'project': self.object, 'author': self.request.user})
        return context"""


