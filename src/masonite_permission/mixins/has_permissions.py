from masoniteorm.query import QueryBuilder
from ..exceptions import PermissionException


class HasPermissions:
    def _permission_query(self):
        """Return a query builder for permissions"""
        from ..models.permission import Permission

        role_id_query = (
            f"select role_user.role_id from role_user where role_user.user_id = {self.id}"
        )

        return Permission.where_in(
            "id",
            lambda q: (
                q.table("model_has_permissions")
                .select("model_has_permissions.permission_id")
                .where_raw(
                    f"""
                    (
                        model_has_permissions.permissionable_type = 'users'
                        and
                        model_has_permissions.permissionable_id = {self.id}
                    )
                    or
                    (
                        model_has_permissions.permissionable_type = 'roles'
                        and
                        model_has_permissions.permissionable_id in (
                            {role_id_query}
                        )
                    )
                """
                )
            ),
        )

    def permissions(self):
        return self._permission_query().get()

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
            self.give_permission_to(permission.slug)

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
            data.append(
                {
                    "permission_id": permission.id,
                    "permissionable_id": self.id,
                    "permissionable_type": self.get_table_name(),
                }
            )

        QueryBuilder().table("model_has_permissions").where("permissionable_id", self.id).where_in(
            "permission_id", permissions.pluck("id")
        ).where("permissionable_type", self.get_table_name()).delete()
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

        QueryBuilder().table("model_has_permissions").where("permissionable_id", self.id).where_in(
            "permission_id", permissions.pluck("id")
        ).where("permissionable_type", self.get_table_name()).delete()

    def _get_permission_ids(self, args):
        from ..models.permission import Permission

        permission_ids = []
        permission_slugs = []

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
                permission_ids.append(permission.id)

        ids = []

        if len(permission_ids) > 0 and len(permission_slugs) > 0:
            ids = (
                Permission.where_raw(f"(id in {permission_ids}) or slug in {permission_slugs}")
                .get()
                .pluck("id")
            )
        elif len(permission_ids) > 0:
            ids = list(Permission.where_in("id", permission_ids).get().pluck("id"))
        elif len(permission_slugs) > 0:
            ids = list(Permission.where_in("slug", permission_slugs).get().pluck("id"))

        return ids

    def sync_permissions(self, *args):
        """Sync permissions from related model"""

        ids = self._get_permission_ids(args)
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

    def has_permission_to(self, permission):
        if type(permission) != str:
            raise PermissionException("permission must be a string!")
        return self._permission_query().where("permissions.slug", permission).count() > 0

    def has_any_permission(self, *args):
        """Check if user has any of the permissions"""

        slugs = []
        if type(args[0]) == list:
            slugs = args[0]
        else:
            slugs = list(args)

        return self._permission_query().where_in("permissions.slug", slugs).count() > 0

    def has_all_permissions(self, *args):
        """Check if user has all of the permissions"""

        slugs = []
        if type(args[0]) == list:
            slugs = args[0]
        else:
            slugs = list(args)

        return self._permission_query().where_in("permissions.slug", slugs).count() == len(slugs)

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
