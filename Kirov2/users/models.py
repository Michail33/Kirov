from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Account(models.Model):
    gender_choices = (('M', 'Mail'), ('F', 'Femail'), ('N/A', 'Not answered'))
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)
    nickname = models.CharField(max_length=100)
    birthdate = models.DateField(null=True)
    gender = models.CharField(choices=gender_choices, max_length=20)
    account_image = models.ImageField(default='default.jpg', upload_to='account_images')
    # pip install Pillow в терминале , если нет библиотеки

    def __str__(self):
        return f"{self.user.username}'s account"

    class Meta:
        ordering = ['user']
        verbose_name = 'Юзер'
        verbose_name_plural = 'Юзеррыы'