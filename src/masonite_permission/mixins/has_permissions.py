from masoniteorm.query import QueryBuilder
from masoniteorm.relationships import belongs_to_many
from masoniteorm.collection.Collection import Collection
from ..exceptions import PermissionException

class HasPermissions():
    
    def permissions(self):
        from ..models.permission import Permission
        
        table = self.get_table_name()
        
        direct_permissions = (
            Permission.join("model_has_permissions as mhp", "mhp.permission_id", "=", "permissions.id")
            .where("mhp.permissionable_id", self.id)
            .where("mhp.permissionable_type", table)
            .select_raw("permissions.*").get()
        )
        
        indirect_permissions = (
            Permission.join("model_has_permissions as mhp", "mhp.permission_id", "=", "permissions.id")
            .where_in("mhp.permissionable_id", self.roles().pluck('id'))
            .where("mhp.permissionable_type", "roles")
            .select_raw("permissions.*").get()
        )
        return Collection(list(direct_permissions) + list(indirect_permissions)).unique("slug")
    
    
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
            self.give_permission_to(permission.slug)
            

    def detach_permission(self, permission):
        """Detach a permission from a role

        Arguments:
            permission {collection or int} -- Permission collection or permission id...
        """
        from ..models.permission import Permission

        permission = Permission.where_slug(permission).first()
        if not permission:
            raise PermissionException(f"Permission: {permission} does not exist!")

        exists = (
            QueryBuilder()
            .table("permission_role")
            .where("role_id", self.id)
            .where("permission_id", permission.id)
            .count()
        )

        if exists:
            self.revoke_permission_to(permission.slug)
        
    
    def give_permission_to(self, *args):
        """Give permission to related model"""
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
        
        QueryBuilder().table("model_has_permissions").where("permissionable_id", self.id).where_in("permission_id", permissions.pluck("id")).where("permissionable_type", self.get_table_name()).delete()
        QueryBuilder().table("model_has_permissions").bulk_create(data)
        
        
    def revoke_permission_to(self, *args):
        """Revoke permission from related model"""
        from ..models.permission import Permission
        
        if type(args[0]) == list:
            args = args[0]
        
        permissions = Permission.where_in("slug", args).get()
        slugs = permissions.pluck("slug")
        diff = set(args) - set(slugs)
        if len(diff) > 0:
            diff_permissions = ", ".join(list(diff))
            raise PermissionException(f"Permission: {diff_permissions} does not exist!")
        
        QueryBuilder().table("model_has_permissions").where("permissionable_id", self.id).where_in("permission_id", permissions.pluck("id")).where("permissionable_type", self.get_table_name()).delete()
        
        
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
        if len(data) > 0:
            QueryBuilder().table("model_has_permissions").bulk_create(data)
        

    def has_permission_to(self, permission):
        if type(permission) != str:
            raise PermissionException("permission must be a string!")

        return self.permissions().pluck("slug").contains(permission)
    
    
    def has_any_permission(self, *args):
        """Check if user has any of the permissions"""
        
        slugs = []
        if type(args[0]) == list:
            slugs = args[0]
        else:
            slugs = list(args)
            
        permissions = self.permissions().pluck("slug")
        
        # get items that are not in the permissions
        # permissions_diff = set(slugs) - set(permissions)
        # if len(permissions_diff) > 0:
        #     diff_permissions = ", ".join(list(permissions_diff))
        #     raise PermissionException(f"Permission: {diff_permissions} does not exist!")
        
        result = set(slugs).intersection(permissions)
    
        return len(result) > 0


    def has_all_permissions(self, *args):
        """Check if user has all of the permissions"""
        
        slugs = []
        if type(args[0]) == list:
            slugs = args[0]
        else:
            slugs = list(args)

        permissions = self.permissions().pluck("slug")
        
        return set(slugs).issubset(permissions) and len(set(slugs) - set(permissions)) == 0
    
    
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