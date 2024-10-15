from django.db import models
from django.contrib.auth.models import User

class EditHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_name = models.CharField(max_length=255)
    edited_image_path = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
