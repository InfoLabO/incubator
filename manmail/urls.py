
from django.urls import path
from manmail import views

urlpatterns = [
    path('', views.email, name="email"),
    path('thanks', views.thanks, name='thanks'),
]
