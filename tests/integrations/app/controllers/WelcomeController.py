"""A WelcomeController Module."""
from masonite.views import View
from masonite.controllers import Controller

from src.masonite_permission.models.permission import Permission
from tests.integrations.app.models.User import User


class WelcomeController(Controller):
    """WelcomeController Controller Class."""

    def show(self, view: View):
        user = User.first()

        return view.render("welcome", {"user": user})

    def test(self):

        permission = Permission.where("slug", "create-user").first()

        permission.sync_roles(["admin", "editor"])

        permission.detach_role("admin")
        permission.attach_role("admin")

        return {
            "roles": permission.roles().serialize(),
        }
