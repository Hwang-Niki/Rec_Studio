from django.contrib.auth.models import AbstractUser
from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Producer(models.Model):
    name = models.CharField(max_length=100)
    albums_produced = models.IntegerField()

    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Manager(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Project(models.Model):
    ALBUM_IMAGE_UPLOAD_PATH = 'album_images/'
    name = models.CharField(max_length=100)
    album_image = models.ImageField(upload_to=ALBUM_IMAGE_UPLOAD_PATH)
    end_date = models.DateField()
    current_status = models.CharField(max_length=20, choices=[
        ('В процессе', 'В процессе'),
        ('Завершен', 'Завершен'),
        ('Отменен', 'Отменен'),
    ])
    performer = models.CharField(max_length=100) # Рассмотрите возможность связать с моделью User

    def __str__(self):
        return self.name

class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('performer', 'Исполнитель'),
        ('producer', 'Продюсер'),
        ('soundman', 'Звукорежисер'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    email = models.EmailField(unique=True, blank=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']  # Убедитесь, что добавили first_name

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
