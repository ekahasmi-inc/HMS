class RoleService:

    @staticmethod
    def assign_role(user, tenant, role):
        ...

    @staticmethod
    def remove_role(user, tenant, role):
        ...

    @staticmethod
    def get_roles(user, tenant):
        ...

    @staticmethod
    def has_role(user, tenant, role_code):
        ...