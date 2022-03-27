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
    
    def permissions(self):
        from ..models.permission import Permission
        
        table = self.get_table_name()
        
        return (
            Permission.join("model_has_permissions as mhp", "mhp.permission_id", "=", "permissions.id")
            .where("mhp.permissionable_id", self.id)
            .where("mhp.permissionable_type", table)
            .select_raw("permissions.*").get()
        )

    def sync_permissions(self, *args):
        """Sync permissions from related model"""
        from ..models.permission import Permission
        
        if type(args[0]) == list:
            args = args[0]
        
        permissions = Permission.where_in("slug", args).get()
        slugs = permissions.pluck("slug")
        diff = set(args) - set(slugs)
        if len(diff) > 0:
            diff_permissions = ", ".join(list(diff))
            raise PermissionException(f"Permission: {diff_permissions} does not exist!")
        
        data = []
        for permission in permissions:
            data.append({
                "permission_id": permission.id, 
                "permissionable_id": self.id,
                "permissionable_type": self.get_table_name()
            })
        
        QueryBuilder().table("model_has_permissions").where("permissionable_id", self.id).where("permissionable_type", self.get_table_name()).delete()
        if (len(data) > 0):
            QueryBuilder().table("model_has_permissions").bulk_create(data)


    def attach_permission(self, permission):
        """Assign a permission to a role

        Arguments:
            permission {collection or int} -- Permission collection or permission id...
        """
        from ..models.permission import Permission
        
        if type(permission) == str:
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
            QueryBuilder().table("model_has_permissions").create({
                "permission_id": permission.id,
                "permissionable_id": self.id,
                "permissionable_type": self.get_table_name()
            })

    def detach_permission(self, permission):
        """Detach a permission from a role

        Arguments:
            permission {collection or int} -- Permission collection or permission id...
        """
        from ..models.permission import Permission
        
        if type(permission) == str:
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
            QueryBuilder().table("model_has_permissions").where("permissionable_id", self.id).where("permissionable_type", self.get_table_name()).where("permission_id", permission.id).delete()