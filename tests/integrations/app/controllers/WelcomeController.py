"""A WelcomeController Module."""
from masonite.views import View
from masonite.controllers import Controller

# from masoniteorm.query import QueryBuilder
# from src.masonite_permission.models.permission import Permission
from src.masonite_permission.models import Role
from tests.integrations.app.models.User import User


class WelcomeController(Controller):
    """WelcomeController Controller Class."""

    def show(self, view: View):
        user = User.first()

        return view.render("welcome", {"user": user})

    def test(self):
        """users = [{
            "name": "John Doe",
            "email": "john@doe.com",
            "password": "capslock",
        }, {
            "name": "Jane Doe",
            "email": "jane@doe.com",
            "password": "capslock",
        }]

        roles = [{
            "name": "Admin",
            "slug": "admin",
        }, {
            "name": "Editor",
            "slug": "editor",
        }, {
            "name": "Reporter",
            "slug": "reporter"
        }]

        permissions = [{
            "name": "Create Post",
            "slug": "create-post",
        }, {
            "name": "Edit Post",
            "slug": "edit-post",
        }, {
            "name": "Delete Post",
            "slug": "delete-post",
        }, {
            "name": "Create User",
            "slug": "create-user",
        }, {
            "name": "Edit User",
            "slug": "edit-user",
        }, {
            "name": "Delete User",
            "slug": "delete-user",
        }]

        QueryBuilder().table("users").bulk_create(users)
        QueryBuilder().table("roles").bulk_create(roles)
        QueryBuilder().table("permissions").bulk_create(permissions)
        """

        user = User.first()
        # role = Role.where("slug", "admin").first()
        # permission = Permission.where("slug", "create-user").first()

        """Role related methods
        Methods:
            role.sync_permissions([permission])
            role.attach_permission(permission)
            role.detach_permission(permission)
        """

        """Permission related methods

        Methods:
            permission.sync_roles([role])
            permission.attach_role(role)
            permission.detach_role(role)
        """

        """User related methods

        Methods:
            user.sync_roles([role])
            user.assign_role(role)
            user.revoke_role(role)
            user.has_role(role)
            user.has_any_role(roles)
            user.has_all_roles(roles)
        """

        # Role.create({
        #     "name": "Driver",
        #     "slug": "driver",
        # })
        return Role.all()
        # role.sync_permissions(Permission.all())
        # return role.permissions
        # user.attach_role(role)
        return user.roles
        return {"result": user.roles}
