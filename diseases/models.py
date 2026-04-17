from django.db import models


class Symptom(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Симптом")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Симптом"
        verbose_name_plural = "Симптоми"


class Disease(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва хвороби")
    description = models.TextField(verbose_name="Опис")
    image = models.ImageField(upload_to='diseases/', verbose_name="Зображення")

    # Зв'язок Many-to-Many
    symptoms = models.ManyToManyField(Symptom, related_name='diseases', verbose_name="Симптоми")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Хвороба"
        verbose_name_plural = "Хвороби"

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Користувач")
    position = models.CharField(max_length=100, verbose_name="Посада/Спеціалізація", blank=True)
    bio = models.TextField(verbose_name="Про себе", blank=True)

    class Meta:
        verbose_name = "Додаткова інформація"
        verbose_name_plural = "Профілі користувачів"

    def __str__(self):
        return f"Профіль: {self.user.username}"
