from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
# 우리의 default 유저
class User(AbstractUser):
    # related_name을 설정하지 않으면 followers_set이라고 해야하는데 말이 안되잖아
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followings")
    
    
class Profile(models.Model):
    description = models.TextField(blank=True)
    nickname = models.CharField(max_length=40, blank=True)
    image = models.ImageField()
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"<{self.user.username}의 프로필> {self.nickname}"