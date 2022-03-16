"""Role Model."""
from masoniteorm.models import Model
from masoniteorm.relationships import belongs_to_many
from masoniteorm.query import QueryBuilder
from masoniteorm.collection.Collection import Collection
from ..exceptions import PermissionException


class Role(Model):
    """Role Model."""

    __primary_key__ = "id"

    __fillable__ = ["name", "slug"]

    @belongs_to_many("role_id", "permission_id", "id", "id")
    def permissions(self):
        """Role can have multiple permissions"""
        from ..models.permission import Permission

        return Permission

    def attach_permission(self, permission):
        """Assign a permission to a role

        Arguments:
            permission {collection or int} -- Permission collection or permission id...
        """
        from ..models.permission import Permission

        if isinstance(permission, int) or isinstance(permission, str):
            permission = Permission.find(int(permission))

        exists = (
            QueryBuilder()
            .table("permission_role")
            .where("role_id", self.id)
            .where("permission_id", permission.id)
            .count()
        )

        if not exists:
            self.attach("permissions", permission)

    def detach_permission(self, permission):
        """Detach a permission from a role

        Arguments:
            permission {collection or int} -- Permission collection or permission id...
        """
        from ..models.permission import Permission

        if isinstance(permission, int) or isinstance(permission, str):
            permission = Permission.find(int(permission))

        exists = (
            QueryBuilder()
            .table("permission_role")
            .where("role_id", self.id)
            .where("permission_id", permission.id)
            .count()
        )

        if exists:
            self.detach("permissions", permission)

    def sync_permissions(self, permissions: list):
        """Sync permissions for a role

        Arguments:
            permissions {list} -- List of permissions collection or permission ids...

        """
        from ..models.permission import Permission

        if type(permissions) != Collection and type(permissions) != list:
            raise PermissionException(
                "Permissions must be a list of collection of permissions or permission ids!"
            )

        if len(permissions) != 0:
            permission = permissions[0]
            if isinstance(permission, int) or isinstance(permission, str):
                permissions = Permission.where_in("id", permissions).get()

        QueryBuilder().table("permission_role").where("role_id", self.id).delete()
        self.save_many("permissions", permissions)
