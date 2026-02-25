from django.urls import path
from friends.views import SendFriendRequestView, IncomingFriendRequestsView, FriendListView, \
    FriendRequestActionView

urlpatterns = [
    path('send/<str:username>/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('requests/', IncomingFriendRequestsView.as_view(), name='incoming-requests'),
    # path('accept/<int:request_id>/', AcceptFriendRequestView.as_view(), name='accept-request'),
    path('list/', FriendListView.as_view(), name='friend-list'),
    path("request/<int:request_id>/", FriendRequestActionView.as_view(), name="friend-request-action"),
]