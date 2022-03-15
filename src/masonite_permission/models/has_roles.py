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

    def attach_role(self, role):
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

    def detatch_role(self, role):
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
