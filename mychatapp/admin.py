from django.contrib import admin
from mychatapp.models import Profile, FriendRequest, Notification, ChatMessage

admin.site.register(Profile)
admin.site.register(FriendRequest)
admin.site.register(Notification)
admin.site.register(ChatMessage)