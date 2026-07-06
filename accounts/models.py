from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email=models.EmailField(max_length=254,unique=True)
    phone=models.CharField(unique=True,blank=True,null=True)
    profile_picture=models.ImageField(upload_to='media/profiles/',blank=True,null=True)
    birth_date=models.DateField(auto_now=False, auto_now_add=False,blank=True,null=True)
    bio=models.TextField(blank=True,null=True)

    def __str__(self):
        return self.username