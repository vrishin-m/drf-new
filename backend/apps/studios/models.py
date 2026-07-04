import uuid
from django.db import models
from django.conf import settings

class Studio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)         
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Membership(models.Model):
    ROLE_CHOICES = [
        ('studio_admin', 'Studio Admin'),
        ('project_lead', 'Project Lead'),
        ('designer', 'Designer'),
        ('writer', 'Writer'),
        ('reviewer', 'Reviewer'),
        ('client_viewer', 'Client Viewer'),
    ]

    id     = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name='memberships')
    user   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='memberships')
    role   = models.CharField(max_length=30, choices=ROLE_CHOICES, default='designer')

    class Meta:
        unique_together = ('studio', 'user')   

    def __str__(self):
        return f"{self.user} @ {self.studio} ({self.get_role_display()})"

StudioMembership = Membership