from django.contrib.auth.decorators import login_required
from django.urls import path
from gallery import views


urlpatterns = [
    path('', views.gallery_home, name='gallery_home'),
    path('photos', views.photo_by_tag, name='photo_by_tag'),
    path('<int:pk>', views.AlbumDetailView.as_view(), name='view_album'),
    path('edit/<int:pk>', views.AlbumEditView.as_view(), name='edit_album'),
    path('<int:album_id>/delete_photo/<int:photo_id>', login_required(views.delete_photo),name='delete_photo'),
    path('delete_album/<int:album_id>', login_required(views.delete_album),name='delete_album'),
    path('edit_photo/<int:pk>', views.PhotoEditView.as_view(), name='edit_photo'),
    path('<int:album_id>/add_photo/', views.PhotoAddView.as_view(), name='add_photo'),
    path('add_album', views.AlbumAddView.as_view(), name='add_album'),
    path('add_tag/', views.TagAddView.as_view(), name='add_tag'),

]
