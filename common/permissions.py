from rest_framework.permissions import BasePermission

from common.choices import UserType


class IsEmployeeUser(BasePermission):
    """
    Custom permission to only allow employee users.
    """

    def has_permission(self, request, view):
        return request.user.type == UserType.EMPLOYER or request.user.is_staff
    
    
    
class IsApplicantUser(BasePermission):
    """
    Custom permission to only allow employee users.
    """

    def has_permission(self, request, view):
        return request.user.type == UserType.APPLICANT or request.user.is_staff
    

class IsAdminUser(BasePermission):
    """
    Custom permission to only allow employee users.
    """

    def has_permission(self, request, view):
        return request.user.is_staff
