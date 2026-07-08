from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Project(models.Model):
    studio = models.ForeignKey('studios.Studio', on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Tag(models.Model):
    studio = models.ForeignKey('studios.Studio', on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    color = models.CharField(max_length=7, default='#888888')

class Task(models.Model):
    STAGE_CHOICES = [('DRAFT','Draft'),('REVIEW','Review'),('REVISION','Revision'),
                      ('APPROVED','Approved'),('COMPLETED','Completed')]
    PRIORITY_CHOICES = [('LOW','Low'),('MEDIUM','Medium'),('HIGH','High'),('URGENT','Urgent')]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='work_items')
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='DRAFT')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_items')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_items')
    tags = models.ManyToManyField(Tag, blank=True)
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class StageTransitionLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='transition_logs')
    from_stage = models.CharField(max_length=20)
    to_stage = models.CharField(max_length=20)
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    changed_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class ProjectAttachment(models.Model):
    project = models.ForeignKey(Project , on_delete=models.CASCADE , related_name="project_attachments")
    file = models.FileField(upload_to='project_attachments/')
    version = models.PositiveIntegerField(default=1)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class TaskAttachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_attachments')
    file = models.FileField(upload_to='attachments/')
    version = models.PositiveIntegerField(default=1)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)