from django.db import models
from django.contrib.auth.models import User

class EditHistory(models.Model):
    """
    Модель EditHistory для хранения информации об изменениях изображений.

    Атрибуты:
    - user (ForeignKey): Ссылка на модель User, представляющая пользователя,
      который внес изменения. При удалении пользователя все связанные записи
      будут также удалены (on_delete=models.CASCADE).

    - image_name (CharField): Название загруженного изображения.

    - edited_image_path (CharField): Путь к отредактированному изображению.

    - timestamp (DateTimeField): Время создания записи. Автоматически заполняется
      текущей датой и временем при добавлении нового объекта.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_name = models.CharField(max_length=255)
    edited_image_path = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
