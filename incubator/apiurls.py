from django.conf.urls import include, url
from rest_framework import routers


import users.views
import projects.views
import space.views


api = routers.DefaultRouter()

api.register(r'users', users.views.UserViewSet)
api.register(r'projects', projects.views.ProjectViewSet)
api.register(r'space/openings', space.views.OpeningsViewSet)
api.register(r'space/pamela', space.views.PamelaViewSet, basename="pamela")

urlpatterns = [
    url(r'^', include(api.urls)),
]
