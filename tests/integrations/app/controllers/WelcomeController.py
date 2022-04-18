"""A WelcomeController Module."""
from masonite.views import View
from masonite.controllers import Controller

from src.masonite_permission.models.permission import Permission
from src.masonite_permission.models.role import Role
from tests.integrations.app.models.User import User
from masoniteorm.expressions import JoinClause
from masoniteorm.query import QueryBuilder


class WelcomeController(Controller):
    """WelcomeController Controller Class."""

    def show(self, view: View):
        user = User.first()
        role = Role.where("slug", "reporter").first()
        user.sync_roles(["admin", 2, "editor", role])

        return view.render("welcome", {"user": user})

    def test(self):
        user = User.first()
        role = Role.first()

        # user.sync_permissions(["create-post", "edit-user"])
        # role.sync_permissions(["create-user", "edit-user", "delete-user"])

        return user.permissions()
        
        # user_two = User.create(
        #     {
        #         "name": "John",
        #         "email": "john@example.com",
        #         "password": "OK",
        #         "phone": "+123456789",
        #     }
        # )

        # user_two.sync_permissions("delete-user")

        return (
            QueryBuilder().table("permissions").select_raw("permissions.id, permissions.name").where_in("id", lambda q: (
                q.table("model_has_permissions")
                .select("model_has_permissions.permission_id")
                .where_raw(f"""
                    (model_has_permissions.permissionable_type = 'users' and model_has_permissions.permissionable_id = {user.id})
                    or
                    (model_has_permissions.permissionable_type = 'roles' and model_has_permissions.permissionable_id in (
                        select role_user.role_id from role_user where role_user.user_id = {user.id}
                    ))
                """)
            )).get()
        )

        return (
            QueryBuilder().table("permissions")
            .select_raw("permissions.id, permissions.name, permissions.slug, users.id")
            .join(pivot_query)
            .join(role_permission_query)
            .join(user_permission_query)
            .group_by("permissions.id, users.id")
            .where("users.id", 1)
            .get()
        )

        user = User.first()
        admin = Role.where("slug", "admin").first()
        
        
        user.attach_permission("edit-user")

        admin.sync_permissions(["create-post", "edit-post", "delete-post"])

        user.sync_roles(['admin', 'editor'])

        return user.permissions()

        return {
            "roles": permission.roles().serialize(),
        }
