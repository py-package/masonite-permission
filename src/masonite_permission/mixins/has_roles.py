from masoniteorm.query import QueryBuilder

from ..exceptions import PermissionException


class HasRoles:
    def _role_query(self):
        from ..models.role import Role

        return Role.join("role_user as ru", "ru.role_id", "=", "roles.id").where(
            "ru.user_id", self.id
        )

    def roles(self):
        return self._role_query().get()

    def has_role_of(self, role):
        """Check if user has a role"""
        if type(role) != str:
            raise PermissionException("role must be a string!")
        return self.roles().where("slug", role).count() > 0

    def has_any_role(self, *args):
        """Check if user has any of the roles"""

        slugs = []
        if type(args[0]) == list:
            slugs = args[0]
        else:
            slugs = list(args)

        return self._role_query().where_in("slug", slugs).count() > 0

    def has_all_roles(self, *args):
        """Check if user has all of the roles"""

        slugs = []
        if type(args[0]) == list:
            slugs = args[0]
        else:
            slugs = list(args)

        return self._role_query().where_in("slug", slugs).count() == len(slugs)

    def _get_role_ids(self, args):
        from ..models.role import Role

        role_ids = []
        role_slugs = []

        if len(args) == 0:
            QueryBuilder().table("role_user").where("user_id", self.id).delete()
            return

        if type(args[0]) == list:
            args = args[0]

        for role in args:
            if isinstance(role, int):
                role_ids.append(role)
            elif isinstance(role, str):
                role_slugs.append(role)
            elif isinstance(role, Role):
                role_ids.append(role.id)

        ids = []

        if len(role_ids) > 0 and len(role_slugs) > 0:
            ids = Role.where_raw(f"(id in {role_ids}) or slug in {role_slugs}").get().pluck("id")
        elif len(role_ids) > 0:
            ids = list(Role.where_in("id", role_ids).get().pluck("id"))
        elif len(role_slugs) > 0:
            ids = list(Role.where_in("slug", role_slugs).get().pluck("id"))

        return ids

    def sync_roles(self, *args):
        """Assign a role to a user"""

        ids = self._get_role_ids(args)
        data = []
        for role in ids:
            data.append({"user_id": self.id, "role_id": role})

        query = QueryBuilder().table("role_user")

        query.where("user_id", self.id).delete()

        if len(data) > 0:
            query.bulk_create(data)

    def assign_role(self, role):
        """Assign a role to a user

        Arguments:
            role {collection or int} -- Role collection or role id...
        """
        from ..models.role import Role

        if isinstance(role, int):
            role = Role.find(int(role))
        elif isinstance(role, str):
            role = Role.where("slug", role).first()

        exists = (
            QueryBuilder()
            .table("role_user")
            .where("user_id", self.id)
            .where("role_id", role.id)
            .count()
        )

        if not exists:
            QueryBuilder().table("role_user").create({"user_id": self.id, "role_id": role.id})

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
            QueryBuilder().table("role_user").where("user_id", self.id).where(
                "role_id", role.id
            ).delete()

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
