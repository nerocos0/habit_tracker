from rest_framework import permissions

class IsAuthenticated(permissions.BasePermission):
    #Проверяем права доступа к объекту

    #До получения объекта проверяем может ли пользователь вообще что-то делать
    def has_permission(self, request, view):
        #Только авторизованные пользователи могут вообще что-то делать
        return request.user.is_authenticated

class IsHabitOwnerOrStaff(permissions.BasePermission):
    #Проверяем права доступа к объекту
    #После получения объекта проверяем может ли пользователь что-то делать с конкретным объектом
    def has_object_permission(self, request, view, obj):
        if request.method == permissions.SAFE_METHODS:   #SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
            return True
        return (obj.user == request.user) or request.user.is_staff

class IsHabitLogOwnerOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == permissions.SAFE_METHODS:
            return True
        return (obj.habit.user == request.user) or request.user.is_staff