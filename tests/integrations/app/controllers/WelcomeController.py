"""A WelcomeController Module."""
from masonite.views import View
from masonite.controllers import Controller

from masoniteorm.query import QueryBuilder
from src.masonite_permission.models.permission import Permission
from src.masonite_permission.models import Role
from tests.integrations.app.models.User import User


class WelcomeController(Controller):
    """WelcomeController Controller Class."""

    def show(self, view: View):
        user = User.first()

        return view.render("welcome", {"user": user})

    def test(self):
        user = User.first()
        
        # user.give_permission_to("create-post", "edit-post")
        # user.give_permission_to("delete-post")
        # user.revoke_permission_to(["delete-post", 'create-post'])
        
        """ role = Role.first()
        
        role.sync_permissions(['create-post', 'edit-post', 'delete-post'])
        role.attach_permission("create-user")
        role.detach_permission("create-post") """
        
        # user.assign_role(role)
        # user.revoke_role(role)
        
        """ return {
            "roles": user.roles().serialize(),
            "permissions": role.permissions().serialize(),
            "has_role": user.has_role_of("admin"),
            "user_permissions": user.permissions().serialize(),
        } """
        
        permission = Permission.where("slug", "create-user").first()
        
        permission.sync_roles(["admin", "editor"])
        
        permission.detach_role("admin")
        permission.attach_role("admin")
        
        return {
            "roles": permission.roles().serialize(),
        }
        
        # user.give_permission_to("create-post", "edit-post")
        
        # QueryBuilder().table("model_has_permissions").create({
        #     "permission_id": 3,
        #     "permissionable_id": role.id,
        #     "permissionable_type": "roles"
        # })
        
        # select p.* from permissions as p,
        #     model_has_permissions as mhp,
        #     users as u,
        #     role_user as ru
        #     where ((mhp.permissionable_id = u.id and mhp.permissionable_type = 'users' and mhp.permission_id = p.id) or
        #     (mhp.permissionable_id = ru.role_id and mhp.permissionable_type = 'roles' and ru.user_id = u.id and mhp.permission_id = p.id)) and
        #     u.id = '1'

        return {
            "data": user.has_permission_to("create-posts"),
            "has_any": user.has_any_permission(["create-post", "edit-post"]),
            "has_all": user.has_all_permissions(["create-post", "edit-post", "delete-post"]),
            "can_any": user.can_("create-post|edit-post|delete-post"),
            "can_all": user.can_("create-post,edit-post,delete-post"),
            "permissions": user.permissions().serialize()
        }
