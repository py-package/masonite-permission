"""Role Model."""
from masoniteorm.models import Model
from masoniteorm.query import QueryBuilder

from ..exceptions import PermissionException


class Role(Model):
    """Role Model."""

    __primary_key__ = "id"

    __fillable__ = ["name", "slug"]

    def permissions(self):
        from ..models.permission import Permission

        table = self.get_table_name()

        return (
            Permission.join(
                "model_has_permissions as mhp", "mhp.permission_id", "=", "permissions.id"
            )
            .where("mhp.permissionable_id", self.id)
            .where("mhp.permissionable_type", table)
            .select_raw("permissions.*")
            .get()
        )

    def sync_permissions(self, *args):
        """Sync permissions from related model"""
        from ..models.permission import Permission

        permission_ids = []
        permission_slugs = []
        found_ids = []

        if len(args) == 0:
            QueryBuilder().table("model_has_permissions").where(
                "permissionable_id", self.id
            ).where("permissionable_type", self.get_table_name()).delete()
            return

        if type(args[0]) == list:
            args = args[0]

        for permission in args:
            if isinstance(permission, int):
                permission_ids.append(permission)
            elif isinstance(permission, str):
                permission_slugs.append(permission)
            elif isinstance(permission, Permission):
                found_ids.append(permission.id)

        permission_by_id = list(Permission.where_in("id", permission_ids).get().pluck("id"))
        permission_by_slug = list(Permission.where_in("slug", permission_slugs).get().pluck("id"))

        ids = list(dict.fromkeys(found_ids + permission_by_id + permission_by_slug))

        data = []
        for permission in ids:
            data.append(
                {
                    "permission_id": permission,
                    "permissionable_id": self.id,
                    "permissionable_type": self.get_table_name(),
                }
            )

        query = QueryBuilder().table("model_has_permissions")

        query.where("permissionable_id", self.id).where(
            "permissionable_type", self.get_table_name()
        ).delete()

        if len(data) > 0:
            query.bulk_create(data)

    def attach_permission(self, permission):
        """Assign a permission to a role

        Arguments:
            permission {collection or int} -- Permission collection or permission id...
        """
        from ..models.permission import Permission

        if isinstance(permission, int):
            permission = Permission.find(permission)
            if not permission:
                raise PermissionException(f"Permission: with id {permission} does not exist!")

        elif isinstance(permission, str):
            permission = Permission.where("slug", permission).first()
            if not permission:
                raise PermissionException(f"Permission: {permission} does not exist!")

        exists = (
            QueryBuilder()
            .table("model_has_permissions")
            .where("permissionable_id", self.id)
            .where("permission_id", permission.id)
            .where("permissionable_type", self.get_table_name())
            .count()
        )

        if not exists:
            QueryBuilder().table("model_has_permissions").create(
                {
                    "permission_id": permission.id,
                    "permissionable_id": self.id,
                    "permissionable_type": self.get_table_name(),
                }
            )

    def detach_permission(self, permission):
        """Detach a permission from a role

        Arguments:
            permission {collection or int} -- Permission collection or permission id...
        """
        from ..models.permission import Permission

        if isinstance(permission, int):
            permission = Permission.find(permission)
            if not permission:
                raise PermissionException(f"Permission: with id {permission} does not exist!")

        elif isinstance(permission, str):
            permission = Permission.where("slug", permission).first()
            if not permission:
                raise PermissionException(f"Permission: {permission} does not exist!")

        exists = (
            QueryBuilder()
            .table("model_has_permissions")
            .where("permissionable_id", self.id)
            .where("permission_id", permission.id)
            .where("permissionable_type", self.get_table_name())
            .count()
        )

        if exists:
            QueryBuilder().table("model_has_permissions").where(
                "permissionable_id", self.id
            ).where("permissionable_type", self.get_table_name()).where(
                "permission_id", permission.id
            ).delete()
