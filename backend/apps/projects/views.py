from rest_framework.decorators import api_view , action
from rest_framework.response import Response
from .models import Project , Task , StageTransitionLog , Comment , Tag , ProjectAttachment , TaskAttachment
from .serializers import ProjectSerializer , TaskSerializer , CommentSerializer , TagSerializer , ProjectAtachmentSerializer , TaskAtachmentSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .permissions import IsAssignedOrHasMinRole , IsStudioMember , HasMinRole 

# ROLE_HIERARCHY = [
#     "client_viewer",
#     "writer",
#     "designer",
#     "reviewer",
#     "project_lead",
#     "studio_admin"
# ]

ALLOWED_TRANSITIONS = {
    'DRAFT': ['REVIEW'],
    'REVIEW': ['REVISION', 'APPROVED'],
    'REVISION': ['REVIEW'],
    'APPROVED': ['COMPLETED'],
    'COMPLETED': [],
}


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated , IsStudioMember , HasMinRole]

    def get_queryset(self):
        qs = Project.objects.all()
        studio_id = self.request.query_params.get('studio')
        if studio_id:
            qs = qs.filter(studio_id = studio_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(created_by = self.request.user)
    required_role= 'project_lead'



class TaskViewSet(viewsets.ModelViewSet):
    serializer_class= TaskSerializer
    permission_classes = [permissions.IsAuthenticated , IsStudioMember , IsAssignedOrHasMinRole ]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['stage', 'priority', 'assigned_to', 'project' , 'tags']
    search_fields = ['title', 'description']

    def get_queryset(self):
        return Task.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(created_by = self.request.user)

    @action(detail=True , methods=['post'])
    def transition(self , request , pk=None):
        item = self.get_object()
        to_stage = request.data.get('to_stage')

        if to_stage not in ALLOWED_TRANSITIONS.get(item.stage , []):
            return Response (
                {"error": f"Cannot move from {item.stage} to {to_stage}"},
                status=400
            )
        
        StageTransitionLog.objects.create(
            task=item, from_stage=item.stage,
            to_stage=to_stage, changed_by=request.user
        )
        item.stage = to_stage
        item.save()
        return Response(TaskSerializer(item).data)
    required_role = 'reviewer'

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated , IsStudioMember ]

    def get_queryset(self):
        qs = Comment.objects.all()
        task_id = self.request.query_params.get('task')
        if task_id:
            qs = qs.filter(task_id= task_id)
        return qs.order_by('created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class= TagSerializer
    permission_classes = [permissions.IsAuthenticated , IsStudioMember]    

    def get_queryset(self):
        qs = Tag.objects.all()
        studio_id = self.request.query_params.get('studio')
        if studio_id:
            qs = qs.filter(studio_id = studio_id)
        return qs

# @api_view(['GET'])
# def get_all_projects(request):
#     projects = Project.objects.all()
#     serializer = ProjectSerializer(projects , many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def get_project_by_id(request , pk):
#     project = get_object_or_404(Project , pk=pk)
#     serializer = ProjectSerializer(project)
#     return Response(serializer.data)

# @api_view(['GET'])
# def get_task_by_ (request , pk):
#     project = get_object_or_404(Project , pk=pk)
#     serializer = ProjectSerializer(project)
#     return Response(serializer.data)


class ProjectAttachmentViewSet(viewsets.ModelViewSet):

    serializer_class = ProjectAtachmentSerializer
    permission_classes = [permissions.IsAuthenticated , IsStudioMember , HasMinRole]

    def get_queryset(self):
        qs = ProjectAttachment.objects.all()
        project_id = self.request.query_params.get('project')
        if project_id:
            qs = qs.filter(project_id=project_id)
        return qs 
    
    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        next_version = ProjectAttachment.objects.filter(project=project).count() + 1 
        serializer.save(uploaded_by=self.request.user , version = next_version)
    required_role = 'project_lead'

class TaskAttachmentViewSet(viewsets.ModelViewSet):

    serializer_class = TaskAtachmentSerializer
    permission_classes = [permissions.IsAuthenticated , IsStudioMember , IsAssignedOrHasMinRole]

    def get_queryset(self):
        qs = TaskAttachment.objects.all()
        task_id = self.request.query_params.get('task')
        if task_id:
            qs = qs.filter(task_id=task_id)
        return qs

    def perform_create(self, serializer):
        task = serializer.validated_data['task']
        next_version = TaskAttachment.objects.filter(task=task).count() + 1
        serializer.save(uploaded_by=self.request.user, version=next_version)
    required_role = 'reviewer'
