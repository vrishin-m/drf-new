from rest_framework.permissions import BasePermission
from ..studios.models import Membership , Studio

ROLE_RANK = {
    'client_viewer': 0,
    'writer': 1,
    'designer': 1,
    'reviewer': 2,
    'project_lead': 3,
    'studio_admin': 4,
}
 
def get_role(user , studio):
    if not user.is_authenticated:
        return None
    m=Membership.objects.filter(user=user , studio=studio).first()
    return m.role if m else None 

def get_studio_for(obj):
    if hasattr(obj , 'project'):       # task , ProjectAttachment
        return obj.project.studio
    if hasattr(obj , 'studio'):       # project , tag 
        return obj.studio
    if hasattr(obj , 'task'):         # stageTransition , comment , TaskAttachment  
        return obj.task.project.studio
    return None 

class IsStudioMember(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            studio_id = request.data.get('studio')
            
            if studio_id:
                return Membership.objects.filter(user=request.user, studio_id=studio_id).exists()

            studio_slug = view.kwargs.get('studio_slug')
            if studio_slug:
                return Membership.objects.filter(user=request.user, studio__slug=studio_slug).exists()

            return False 
            
        return True
class HasMinRole(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('GET' , 'HEAD' , 'OPTIONS'):      #reading is always allowed , is user is a part of studio 
            return True 
        studio = get_studio_for(obj)
        role = get_role(user=request.user , studio=studio)
        if role is None:
            return False
        required = getattr(view, 'required_role' , 'writer')
        return ROLE_RANK[role] >= ROLE_RANK[required]

class IsAssignedOrHasMinRole(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('GET' , 'HEAD' , 'OPTIONS'):
            return True 
        if getattr(obj , 'assigned_to_id' , None ) == request.user.id:
            return True
        studio = get_studio_for(obj)
        role = get_role(request.user, studio)
        required = getattr(view, 'required_role', 'reviewer')
        return role is not None and ROLE_RANK[role] >= ROLE_RANK[required]        
    