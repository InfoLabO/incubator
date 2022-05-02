from django.urls import path

from materials import views

urlpatterns = [
    path('', views.own_materials, name='materials'),

]