from django.urls import path


from storage import views

urlpatterns = [
    path('', views.StorageHomeView, name='storage_home'),
]
