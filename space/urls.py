from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (pamela_list, status_change, DeleteMACView,
                    openings_data, full_pamela, get_user_mac, get_mac_user,)


urlpatterns = [
    path('pamela', pamela_list, name='pamela_list'),
    path('change_status', status_change, name='change_status'),
    path('remove_mac/<int:pk>', login_required(DeleteMACView.as_view()), name="delete_mac"),
    path('openings_data', openings_data, name='openings_graph_data'),
    path('private_pamela.json', full_pamela, name='private_pamela'),
    path('user_mac.json', get_user_mac, name='user_mac'),
    path('mac_user.json', get_mac_user, name='mac_user'),

]
