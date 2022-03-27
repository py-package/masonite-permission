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

    def roles(self):
        from ..models.role import Role
        
        return (
            Role.join("model_has_permissions as mhp", "mhp.permissionable_id", "=", "roles.id")
            .where("mhp.permission_id", self.id)
            .where("mhp.permissionable_type", "roles")
            .select_raw("roles.*").get()
        )

    def sync_roles(self, *args):
        """Sync roles from related model"""
        from ..models.role import Role
        
        if type(args[0]) == list:
            args = args[0]
        
        roles = Role.where_in("slug", args).get()
        slugs = roles.pluck("slug")
        diff = set(args) - set(slugs)
        
        if len(diff) > 0:
            diff_roles = ", ".join(list(diff))
            raise PermissionException(f"Role: {diff_roles} does not exist!")
        
        data = []
        for role in roles:
            data.append({
                "permission_id": self.id, 
                "permissionable_id": role.id,
                "permissionable_type": "roles"
            })
        
        QueryBuilder().table("model_has_permissions").where("permissionable_type", "roles").where("permission_id", self.id).delete()
        if (len(data) > 0):
            QueryBuilder().table("model_has_permissions").bulk_create(data)


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

        exists = (
            QueryBuilder()
            .table("model_has_permissions")
            .where("permissionable_id", role.id)
            .where("permission_id", self.id)
            .where("permissionable_type", "roles")
            .count()
        )

        if not exists:
            QueryBuilder().table("model_has_permissions").create({
                "permission_id": self.id,
                "permissionable_id": role.id,
                "permissionable_type": "roles"
            })

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

        exists = (
            QueryBuilder()
            .table("model_has_permissions")
            .where("permissionable_id", role.id)
            .where("permission_id", self.id)
            .where("permissionable_type", "roles")
            .count()
        )

        if exists:
            QueryBuilder().table("model_has_permissions").where("permissionable_id", role.id).where("permissionable_type", "roles").where("permission_id", self.id).delete()