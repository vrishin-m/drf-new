from rest_framework.permissions import BasePermission
from .models import Membership, Studio

ROLE_HIERARCHY = [
    "client_viewer",
    "writer",
    "designer",
    "reviewer",
    "project_lead",
    "studio_admin"
]


def get_membership(user, studio_slug):
    if not user.is_authenticated:
        return None

    try:
        studio = Studio.objects.get(slug=studio_slug)

        return Membership.objects.get(
            user=user,
            studio=studio
        )

    except (Membership.DoesNotExist, Studio.DoesNotExist):
        return None


def has_role(user, studio_slug, *roles):
    m = get_membership(user, studio_slug)
    return m and m.role in roles


def has_min_role(user, studio_slug, min_role):
    m = get_membership(user, studio_slug)
    if not m:
        return False

    return (
        ROLE_HIERARCHY.index(m.role) >= ROLE_HIERARCHY.index(min_role)
    )


class IsStudioMember(BasePermission):
    def has_permission(self, request, view):
        studio_slug = view.kwargs.get("slug")
        return bool(
            get_membership(
                request.user,
                studio_slug
            )
        )


class IsStudioAdmin(BasePermission):
    def has_permission(self, request, view):
        studio_slug = view.kwargs.get("slug")

        return has_role(
            request.user,
            studio_slug,
            'studio_admin'
        )


class IsProjectLeadOrAbove(BasePermission):
    def has_permission(self, request, view):
        studio_slug = view.kwargs.get("slug")

        return has_min_role(
            request.user,
            studio_slug,
            'project_lead'
        )


class IsReviewerOrAbove(BasePermission):
    def has_permission(self, request, view):
        studio_slug = view.kwargs.get("slug")

        return has_min_role(
            request.user,
            studio_slug,
            'reviewer'
        )


class CannotWrite(BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True

        studio_slug = view.kwargs.get("slug")
        return has_min_role(
            request.user,
            studio_slug,
            'writer'
        )