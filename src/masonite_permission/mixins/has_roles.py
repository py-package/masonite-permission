from masoniteorm.relationships import belongs_to_many
from masoniteorm.query import QueryBuilder
from masoniteorm.collection.Collection import Collection

from ..exceptions import PermissionException


class HasRoles():
    
    def roles(self):
        from ..models.role import Role
        
        return Role.join("role_user as ru", "ru.role_id", "=", "roles.id").where("ru.user_id", self.id).get()

    def has_role_of(self, role):
        """Check if user has a role"""
        if type(role) != str:
            raise PermissionException("role must be a string!")

        return self.roles().pluck("slug").contains(role)

    
    def has_any_role(self, *args):
        """Check if user has any of the roles"""

        slugs = []
        if type(args[0]) == list:
            slugs = args[0]
        else:
            slugs = list(args)

        roles = self.roles().pluck("slug")

        result = set(slugs).intersection(roles)
    
        return len(result) > 0

    
    def has_all_roles(self, *args):
        """Check if user has all of the roles"""
        
        slugs = []
        if type(args[0]) == list:
            slugs = args[0]
        else:
            slugs = list(args)

        roles = self.roles().pluck("slug")
        
        return set(slugs).issubset(roles) and len(set(slugs) - set(roles)) == 0


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
            QueryBuilder().table("role_user").where("user_id", self.id).where("role_id", role.id).delete()


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
