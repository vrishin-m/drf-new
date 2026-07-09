from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class MyUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        
        user.set_password(password) # This automatically hashes the password!
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, full_name, password, **extra_fields)



class Account(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,
        editable=False
    )

    email = models.EmailField( 
        unique=True
    )

    full_name = models.CharField(
        max_length=100
    )
    objects = MyUserManager() 
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["fullname" ]

    def __str__(self):
        return self.email

