from django.db import models
from django.contrib.auth.models import User

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(blank=True,max_length=13)
    def __str__(self):
        """
        :return: user's username
        """
        return self.user.username
