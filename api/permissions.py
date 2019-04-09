from rest_framework import permissions

class UserAccessPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print("Roles: ", request.user.profile.role)
        return request.user.profile.role != 'USER'
        # return False
    
    def has_object_permission(self, request, view, obj):
        print("Roles: ", request.user.profile.role)
        return request.user.profile.role != 'USER'

class EntryAccessPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner.profile == request.user.id