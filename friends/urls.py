from django.urls import path
from friends.views import SendFriendRequestView

urlpatterns = [
    path('send/<str:username>/', SendFriendRequestView.as_view(), name='send-friend-request'),
]