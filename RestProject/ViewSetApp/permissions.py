
from rest_framework.permissions import BasePermission , SAFE_METHODS

class OrderPermission(BaseException):

    def has_permission(self,request,view):
        if request.method == SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH']:
            return obj.user == request.user
        return True