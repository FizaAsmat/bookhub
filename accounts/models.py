from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    Role_Choices=(
        ('admin', 'Admin'),
        ('librarian', 'Librarian'),
        ('member', 'Member'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=Role_Choices, default='member')

    def __str__(self):
        return f'{self.user.username} - {self.role}'