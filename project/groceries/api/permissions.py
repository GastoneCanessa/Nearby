from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            try:
                return obj.user == request.user
            except AttributeError:
                return obj.greengrocer == request.user.greengrocer  

        
