from django.db import models
from django.utils import timezone


class User(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    def get_title(self):
        return self.title

    def get_content(self):
        return self.content