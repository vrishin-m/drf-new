from rest_framework import serializers
from .models import StageTransitionLog,Project , Tag , Task , Comment , TaskAttachment , ProjectAttachment

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'studio', 'name', 'description', 'created_by', 'is_archived', 'created_at']
        read_only_fields = ['created_by', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'project', 'title', 'description',  'stage',
                  'priority', 'assigned_to', 'created_by', 'tags', 'deadline',
                  'created_at', 'updated_at']
        read_only_fields = ['created_by', 'stage', 'created_at', 'updated_at']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'task', 'author', 'body', 'created_at']
        read_only_fields = ['author', 'created_at']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model= Tag
        fields=['studio' , 'color' , 'name']

class ProjectAtachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAttachment
        fields = ['id', 'project', 'file', 'version', 'uploaded_by', 'uploaded_at']
        read_only_fields = ['version', 'uploaded_by', 'uploaded_at']

class TaskAtachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAttachment
        fields = ['id', 'task', 'file', 'version', 'uploaded_by', 'uploaded_at']
        read_only_fields = ['version', 'uploaded_by', 'uploaded_at']