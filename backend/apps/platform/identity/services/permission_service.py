class PermissionService:

    @staticmethod
    def has_permission(user, tenant, permission_code) -> bool:
        ...

    @staticmethod
    def get_permissions(user, tenant):
        ...

    @staticmethod
    def has_any_permission(user, tenant, permissions):
        ...

    @staticmethod
    def has_all_permissions(user, tenant, permissions):
        ...