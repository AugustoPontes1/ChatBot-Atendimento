from django.db import models


USER_TYPE_CHOICES = [
    ("A", "Usuário A"),
    ("B", "Usuário B"),
]

class Message(models.Model):
    user_sender = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    user_text = models.TextField(null=True, blank=True)
    bot_text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
