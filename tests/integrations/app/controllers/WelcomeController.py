"""A WelcomeController Module."""
from masonite.views import View
from masonite.controllers import Controller

from src.masonite_permission.models.permission import Permission
from src.masonite_permission.models.role import Role
from tests.integrations.app.models.User import User


class WelcomeController(Controller):
    """WelcomeController Controller Class."""

    def show(self, view: View):
        user = User.first()
        role = Role.where("slug", "reporter").first()
        user.sync_roles(["admin", 2, "editor", role])

        return view.render("welcome", {"user": user})

    def test(self):

        permission = Permission.where("slug", "create-user").first()

        permission.sync_roles(["admin", "editor", 3])

        permission.detach_role("admin")
        permission.attach_role("admin")

        return {
            "roles": permission.roles().serialize(),
        }
