from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

from e_motion.accounts.validators import CapitalizedValidator


class AppUser(AbstractUser):
    first_name = models.CharField(
        max_length=150,
        validators=[CapitalizedValidator()],  # Apply the validator
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        validators=[CapitalizedValidator()],  # Apply the validator
        blank=True
    )

    def get_full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        elif self.first_name or self.last_name:
            return self.first_name or self.last_name

        return self.username
