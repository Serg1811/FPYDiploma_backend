import logging

from rest_framework import permissions

logger = logging.getLogger("main")


class IsOwnerOrAdmin(permissions.BasePermission): 
    
    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated):
            logger.warning(f"Запрос {view.action} от неавторизованного пользователя ")
            return False

        user = request.user
        logger.info(f'user={type(user.id)}')
        requested_user_id = request.query_params.get('user', None)
        logger.info(f'user.is_staff={user.is_staff}')
        logger.info(f'requested_user_id={type(requested_user_id)}')
        logger.info(user.id == requested_user_id)        
        if user.is_staff:
            logger.info(f"Запрос {view.action} от АДМИНА")
            return True
        elif requested_user_id and str(user.id) != requested_user_id:
            logger.warning(f"Запрос {view.action} в чужое хранилище от НЕ админа")
            return False

        logger.info(f"Запрос {view.action} в свое хранилище")
        return True

    def has_object_permission(self, request, view, obj):
        if not bool(request.user and request.user.is_authenticated):
            logger.info(f"Запрос {view.action} от неавторизованного пользователя ")
            return False
        user = request.user == obj.user
        is_admin = request.user.is_staff
        if user or is_admin:
            logger.info(f"Запрос {view.action} {'своего файла' if user else 'чужого файла от админа'}")
            return True
        else:
            logger.info(f"Запрос {view.action} чужого файла НЕ от админа ")
            return False
