from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
import uuid

class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email=None, name=None, password=None):
        """create a new user profile"""
        if not email:
            raise ValueError("User must have an email address")
        if not name:
            """ Generating random unique name if not given """
            name = uuid.uuid4().hex[:12].upper()
        if not password:
            raise IOError("Password must be given!!!")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """created and save a new superuser with given details"""

        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    EMAIL_FIELD = 'email'


    def get_username(self):
        """Retrieve username of user"""
        return self.email

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def __str__(self):
        """Return string represention of our user"""
        return self.email
