from django.db import models


USER_TYPE_CHOICES = [
    ("A", "Usuário A"),
    ("B", "Usuário B"),
]

class Message(models.Model):
    sender = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
