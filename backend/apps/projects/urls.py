from rest_framework.routers import DefaultRouter
from .views import (
    CommentViewSet,
    ProjectAttachmentViewSet,
    ProjectViewSet,
    TagViewSet,
    TaskAttachmentViewSet,
    TaskViewSet,
)

router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='project')
router.register('work-items', TaskViewSet, basename='workitem')
router.register('comments', CommentViewSet, basename='comment')
router.register('project-attachments', ProjectAttachmentViewSet, basename='project-attachment')
router.register('task-attachments', TaskAttachmentViewSet, basename='task-attachment')
router.register('tags', TagViewSet, basename='tag')

urlpatterns = router.urls
