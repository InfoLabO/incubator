from django.shortcuts import render

from materials.models import Material


def materials_home(request):
    materials = Material.objects.all()
    return render(request, "materials_home.html", {
        "materials": materials,
    })

