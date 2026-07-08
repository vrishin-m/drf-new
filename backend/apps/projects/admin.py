# myapp/admin.py
from django.contrib import admin
from .models import Project, Task, Tag , Comment , TaskAttachment , ProjectAttachment , StageTransitionLog 

admin.site.register([Project, Task, Tag , Comment , TaskAttachment , ProjectAttachment , StageTransitionLog ])
