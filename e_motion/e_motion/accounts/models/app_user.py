from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


class AppUser(AbstractUser):
    def get_full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
