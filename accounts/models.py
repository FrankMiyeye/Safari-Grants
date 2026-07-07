from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = [
        ('tourist', 'Tourist / Traveler'),
        ('student', 'Student / Researcher'),
        ('professional', 'Professional'),
        ('ngo', 'NGO / Organization'),
        ('operator', 'Tour Operator'),
    ]

    email = models.EmailField(unique=True)
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPES,
        default='tourist'
    )
    phone = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )
    bio = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()