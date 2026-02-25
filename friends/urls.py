from django.urls import path
from friends.views import SendFriendRequestView, FriendListView, FriendRequestActionView, PendingFriendRequestsView

urlpatterns = [
    path('send/<str:username>/', SendFriendRequestView.as_view(), name='send-friend-request'),
    # path('requests/', IncomingFriendRequestsView.as_view(), name='incoming-requests'),
    # path('accept/<int:request_id>/', AcceptFriendRequestView.as_view(), name='accept-request'),
    path('list/', FriendListView.as_view(), name='friend-list'),
    path("request/<int:request_id>/", FriendRequestActionView.as_view(), name="friend-request-action"),
    path('requests/', PendingFriendRequestsView.as_view(), name='pending-requests'),
]