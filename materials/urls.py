from django.urls import path

import materials.views
from materials import views

urlpatterns = [
    path('', materials.views.materials_home, name='materials_home'),
    path('<int:pk>', views.ProjectDetailView.as_view(), name='view_project'),

]