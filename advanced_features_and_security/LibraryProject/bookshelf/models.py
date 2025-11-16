from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to="profile_photos/", null=True, blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username


# Example model with permissions
class Report(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    class Meta:
        permissions = [
            ("can_view", "Can view reports"),
            ("can_create", "Can create reports"),
            ("can_edit", "Can edit reports"),
            ("can_delete", "Can delete reports"),
        ]

    def __str__(self):
        return self.title
