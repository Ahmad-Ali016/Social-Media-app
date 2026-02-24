from django.urls import path

from profiles.views import MyProfileView, UserProfileView

urlpatterns = [
    path('me/', MyProfileView.as_view(), name='my-profile'),
    path('<str:username>/', UserProfileView.as_view(), name='user-profile'),
]