from django.contrib import admin

from friends.models import FriendRequest, Friendship


# Register your models here.

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):

    # Admin configuration for Friend Requests

    list_display = (
        "id",
        "sender",
        "receiver",
        "status",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "sender__email",
        "receiver__email",
        "sender__username",
        "receiver__username",
    )

    # ordering = ("-created_at",)

    readonly_fields = ("created_at", "updated_at")

@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):

    # Admin configuration for Accepted Friendships

    list_display = (
        "id",
        "user1",
        "user2",
        "created_at",
    )

    search_fields = (
        "user1__email",
        "user2__email",
    )

    ordering = ("-created_at",)

    readonly_fields = ("created_at",)