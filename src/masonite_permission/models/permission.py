"""Permission Model."""
from masoniteorm.models import Model
from masoniteorm.relationships import belongs_to_many
from masoniteorm.query import QueryBuilder
from masoniteorm.collection.Collection import Collection
from ..exceptions import PermissionException


class Permission(Model):
    """Permission Model."""

    __primary_key__ = "id"

    __fillable__ = ["name", "slug"]

    @belongs_to_many("permission_id", "role_id", "id", "id")
    def roles(self):
        """Permission can be in multiple roles"""
        from ..models.role import Role

        return Role

    def attach_role(self, role):
        """Assign a role to a permission

        Arguments:
            role {collection or int} -- Role collection or role id...
        """
        from ..models.role import Role

        if isinstance(role, int) or isinstance(role, str):
            role = Role.find(int(role))

        exists = (
            QueryBuilder()
            .table("permission_role")
            .where("permission_id", self.id)
            .where("role_id", role.id)
            .count()
        )

        if not exists:
            self.attach("roles", role)

    def detach_role(self, role):
        """Detach a role from a permission

        Arguments:
            role {collection or int} -- Role collection or role id...
        """
        from ..models.role import Role

        if isinstance(role, int) or isinstance(role, str):
            role = Role.find(int(role))

        exists = (
            QueryBuilder()
            .table("permission_role")
            .where("permission_id", self.id)
            .where("role_id", role.id)
            .count()
        )

        if exists:
            self.detach("roles", role)

    def sync_roles(self, roles: list):
        """Sync roles for a role

        Arguments:
            roles {list} -- List of roles collection or role ids...

        """
        from ..models.role import Role

        if type(roles) != Collection and type(roles) != list:
            raise PermissionException("Roles must be a list of collection of roles or role ids!")

        if len(roles) != 0:
            role = roles[0]
            if isinstance(role, int) or isinstance(role, str):
                roles = Role.where_in("id", roles).get()

        QueryBuilder().table("permission_role").where("permission_id", self.id).delete()
        self.save_many("roles", roles)
