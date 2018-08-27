from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
# Create your models here.

AGGREGATE_CHOICE = ['daily', 'weekly', 'monthly']

class UserProfileManager(BaseUserManager):
    """Helps Django work with our custom model. """

    def create_user(self, email, name, password=None):
        """Create a new user profile object."""
        if not email:
            raise ValueError("Users must have an email address.")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, name, password):
        """Create and saves a new superuser with given details"""

        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self.db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Represent a "user profiles" inside our system"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Used to get a users full name"""
        
        return self.name

    def get_short_name(self):
        """Used to get a users short name"""

        return self.name

    def __str__(self):
        """convert the object to a string"""

        return self.email

class Sales(models.Model):
    """
    Represent sales model
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    purchased_date = models.DateTimeField('purchased date')
    amount = models.IntegerField()