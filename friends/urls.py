from django.urls import path
from friends.views import SendFriendRequestView, IncomingFriendRequestsView, AcceptFriendRequestView, FriendListView

urlpatterns = [
    path('send/<str:username>/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('requests/', IncomingFriendRequestsView.as_view(), name='incoming-requests'),
    path('accept/<int:request_id>/', AcceptFriendRequestView.as_view(), name='accept-request'),
    path('list/', FriendListView.as_view(), name='friend-list'),
]