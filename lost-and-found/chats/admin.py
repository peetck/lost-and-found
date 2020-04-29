from django.contrib import admin

from .models import Chat, Message

# Register your models here.

class ChatAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'theme',
    ]

class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'message',
        'chat',
        'to',
        'timestamp',
        'seen'
    ]

admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)