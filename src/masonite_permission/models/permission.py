"""Permission Model."""
from masoniteorm.models import Model
from masoniteorm.query import QueryBuilder
from ..exceptions import PermissionException


class Permission(Model):
    """Permission Model."""

    __primary_key__ = "id"

    __fillable__ = ["name", "slug"]

    def roles(self):
        from ..models.role import Role

        return (
            Role.join("model_has_permissions as mhp", "mhp.permissionable_id", "=", "roles.id")
            .where("mhp.permission_id", self.id)
            .where("mhp.permissionable_type", "roles")
            .select_raw("roles.*")
            .get()
        )

    def sync_roles(self, *args):
        """Sync roles from related model"""
        from ..models.role import Role

        role_ids = []
        role_slugs = []
        found_ids = []

        if len(args) == 0:
            QueryBuilder().table("model_has_permissions").where(
                "permissionable_type", "roles"
            ).where("permission_id", self.id).delete()
            return

        if type(args[0]) == list:
            args = args[0]

        for role in args:
            if isinstance(role, int):
                role_ids.append(role)
            elif isinstance(role, str):
                role_slugs.append(role)
            elif isinstance(role, Role):
                found_ids.append(role.id)

        role_by_id = list(Role.where_in("id", role_ids).get().pluck("id"))
        role_by_slug = list(Role.where_in("slug", role_slugs).get().pluck("id"))

        ids = list(dict.fromkeys(found_ids + role_by_id + role_by_slug))

        data = []
        for role in ids:
            data.append(
                {
                    "permission_id": self.id,
                    "permissionable_id": role,
                    "permissionable_type": "roles",
                }
            )

        query = QueryBuilder().table("model_has_permissions")

        query.where("permissionable_type", "roles").where("permission_id", self.id).delete()

        if len(data) > 0:
            query.bulk_create(data)

    def attach_role(self, role):
        """Assign a role to a role

        Arguments:
            role {collection or str} -- Role collection or role slug...
        """
        from ..models.role import Role

        if type(role) == str:
            role = Role.where("slug", role).first()
            if not role:
                raise PermissionException(f"Role: {role} does not exist!")
        elif type(role) == int:
            role = Role.find(role)
            if not role:
                raise PermissionException(f"Role: with id {role} does not exist!")

        exists = (
            QueryBuilder()
            .table("model_has_permissions")
            .where("permissionable_id", role.id)
            .where("permission_id", self.id)
            .where("permissionable_type", "roles")
            .count()
        )

        if not exists:
            QueryBuilder().table("model_has_permissions").create(
                {
                    "permission_id": self.id,
                    "permissionable_id": role.id,
                    "permissionable_type": "roles",
                }
            )

    def detach_role(self, role):
        """Detach a role from a permission

        Arguments:
            role {collection or int} -- Role collection or role slug...
        """
        from ..models.role import Role

        if type(role) == str:
            role = Role.where("slug", role).first()
            if not role:
                raise PermissionException(f"Role: {role} does not exist!")
        elif type(role) == int:
            role = Role.find(role)
            if not role:
                raise PermissionException(f"Role: with id {role} does not exist!")

        exists = (
            QueryBuilder()
            .table("model_has_permissions")
            .where("permissionable_id", role.id)
            .where("permission_id", self.id)
            .where("permissionable_type", "roles")
            .count()
        )

        if exists:
            QueryBuilder().table("model_has_permissions").where(
                "permissionable_id", role.id
            ).where("permissionable_type", "roles").where("permission_id", self.id).delete()
