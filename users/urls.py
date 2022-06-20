
from django.urls import path
from django.contrib.auth.decorators import login_required
from users import views

urlpatterns = [
    path('profile', login_required(views.CurrentUserDetailView.as_view()), name='profile'),
    path('edit', login_required(views.UserEditView.as_view()), name='user_edit'),
    path('show_pamela', login_required(views.show_pamela), name='show_pamela'),
    path('hide_pamela', login_required(views.hide_pamela), name='hide_pamela'),
    path('activer_newsletter', login_required(views.on_newsletter), name='activer_newsletter'),
    path('desactiver_newsletter', login_required(views.off_newsletter), name='desactiver_newsletter'),
    path('<str:slug>', views.UserDetailView.as_view(), name='user_profile'),
    path('login/', views.login_view, name="login_view"),
    path('register/', views.RegisterView, name="register"),
    path('passwd/', login_required(views.change_passwd), name="chg_passwd"),
    path('admin/user/<int:id>/change_password', views.admin_change_passwd, name="admin_change_passwd"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('delete/', views.delete, name='delete')

]
