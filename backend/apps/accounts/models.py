from django.db import models
import uuid

class Account(models.Model):
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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["fullname" ]

    def __str__(self):
        return self.email

