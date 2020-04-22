from django.db import models
from django.contrib.auth.models import User
# chats app

# Create your models here.

class Chat(models.Model):
    THEME = (
        ('light', "Light"),
        ('dark', "Dark")
    )
    theme = models.CharField(choices=THEME, max_length=255, default='light')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Message(models.Model):
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    to = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.message