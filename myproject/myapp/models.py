from django.db import models

class Plan(models.Model):
    username = models.CharField(max_length=20)
    tools = models.CharField(max_length=1000)

    def save(self, *args, **kwargs):
        # Дополнительная обработка перед сохранением модели
        super().save(*args, **kwargs)
