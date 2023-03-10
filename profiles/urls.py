from . import views
from django.urls import path


urlpatterns = [
    path('',views.ProfileListView.as_view(),name='all_profiles_view'),
    path('my_profile/',views.my_profile_view,name='my_profile_view'),
    path('my_invites/',views.invites_received_view,name='my_invites_view'),
    path('to_invite/',views.invite_profiles_list_view,name='invite_profiles_view'),
    path('send_invite/',views.sender_invatation,name='send_invite'),
    path('remove_friend/',views.remove_form_friends,name='remove_friend'),
    path('<slug:slug>/',views.ProfileDetailView.as_view(),name='profile_detail_view'),
    path('my_invites/accept/',views.accept_invitation,name='accept_invitation'),
    path('my_invites/reject/',views.reject_invitation,name='reject_invitation'),
]
