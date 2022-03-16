from masoniteorm.relationships import belongs_to_many
from masoniteorm.query import QueryBuilder
from masoniteorm.collection.Collection import Collection

from ..exceptions import PermissionException


class HasRoles:
    @belongs_to_many("user_id", "role_id", "id", "id")
    def roles(self):
        """User can have multiple roles"""
        from ..models.role import Role

        return Role

    def permissions(self):
        """User can have multiple permissions"""
        from ..models.permission import Permission

        roles = self.roles.pluck("id")
        return (
            Permission.join("permission_role as pr", "pr.permission_id", "=", "id")
            .where_in("pr.role_id", roles)
            .select_raw("permissions.*")
            .get()
        )

    def has_role(self, role):
        """Check if user has a role"""
        if type(role) != str:
            raise PermissionException("role must be a string!")

        return self.roles.pluck("slug").contains(role)

    def has_any_role(self, roles):
        """Check if user has any of the roles"""
        from ..models.role import Role

        if type(roles) != Collection and type(roles) != list:
            raise PermissionException("roles must be a collection of roles or list of role ids!")

        if len(roles) != 0:
            role = roles[0]
            if isinstance(role, str):
                roles = Role.where_in("slug", roles).get().pluck("slug")

        slugs = set(self.roles.pluck("slug"))

        return len(slugs.intersection(roles)) > 0

    def has_all_roles(self, roles):
        """Check if user has all of the roles"""

        if roles is None or len(roles) == 0 or type(roles) != list:
            raise PermissionException("roles must be list of role slugs!")

        slugs = self.roles.pluck("slug")
        return set(roles).issubset(slugs) and len(set(roles) - set(slugs)) == 0

    def sync_roles(self, roles):
        """Assign a role to a user"""
        from ..models.role import Role

        if type(roles) != Collection and type(roles) != list:
            raise PermissionException("roles must be a collection of roles or list of role ids!")

        if len(roles) != 0:
            role = roles[0]
            if isinstance(role, int) or isinstance(role, str):
                roles = Role.where_in("id", roles).get()

        QueryBuilder().table("role_user").where("user_id", self.id).delete()
        self.save_many("roles", roles)

    def assign_role(self, role):
        """Assign a role to a user

        Arguments:
            role {collection or int} -- Role collection or role id...
        """
        from ..models.role import Role

        if isinstance(role, int) or isinstance(role, str):
            role = Role.find(int(role))

        exists = (
            QueryBuilder()
            .table("role_user")
            .where("user_id", self.id)
            .where("role_id", role.id)
            .count()
        )

        if not exists:
            self.attach("roles", role)

    def revoke_role(self, role):
        """Detach a role from a user

        Arguments:
            role {collection or int} -- Role collection or role id...
        """
        from ..models.role import Role

        if isinstance(role, int) or isinstance(role, str):
            role = Role.find(int(role))

        exists = (
            QueryBuilder()
            .table("role_user")
            .where("user_id", self.id)
            .where("role_id", role.id)
            .count()
        )

        if exists:
            self.detach("roles", role)

    def has_permission(self, permission):
        """Check if user has a permission"""
        if type(permission) != str:
            raise PermissionException("permission must be a string!")

        return self.permissions().pluck("slug").contains(permission)

    def has_any_permission(self, permissions):
        """Check if user has any of the permissions"""
        from ..models.permission import Permission

        if type(permissions) != Collection and type(permissions) != list:
            raise PermissionException(
                "argument must be a collection of permissions or list of permission ids!"
            )

        if len(permissions) != 0:
            permission = permissions[0]
            if isinstance(permission, str):
                permissions = Permission.where_in("slug", permissions).get().pluck("slug")

        slugs = set(self.permissions().pluck("slug"))

        return len(slugs.intersection(permissions)) > 0

    def has_all_permissions(self, permissions):
        """Check if user has all of the permissions"""

        if permissions is None or len(permissions) == 0 or type(permissions) != list:
            raise PermissionException("permissions must be list of permission slugs!")

        slugs = self.permissions().pluck("slug")
        return set(permissions).issubset(slugs) and len(set(permissions) - set(slugs)) == 0

    def can_(self, permissions):
        """Check if user has a permission"""
        if type(permissions) != str:
            raise PermissionException("permission must be a string!")

        action = "all"  # can be all or any

        # check if permissions contains a comma
        if "," in permissions:
            permissions = permissions.split(",")
        elif "|" in permissions:
            action = "any"
            permissions = permissions.split("|")
        else:
            permissions = [permissions]

        if action == "all":
            return self.has_all_permissions(permissions)

        if action == "any":
            return self.has_any_permission(permissions)

    def is_(self, roles):
        """Check if user has a role"""
        if type(roles) != str:
            raise PermissionException("role must be a string!")

        action = "all"  # can be all or any

        # check if permissions contains a comma
        if "," in roles:
            roles = roles.split(",")
        elif "|" in roles:
            action = "any"
            roles = roles.split("|")
        else:
            roles = [roles]

        if action == "all":
            return self.has_all_roles(roles)

        if action == "any":
            return self.has_any_role(roles)
