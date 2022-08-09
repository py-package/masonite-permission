"""A WelcomeController Module."""
from masonite.views import View
from masonite.controllers import Controller

from tests.integrations.app.models.User import User


class WelcomeController(Controller):
    """WelcomeController Controller Class."""

    def show(self, view: View):
        user = User.first()
        return view.render("welcome", {"user": user})

    def test(self):
        user = User.first()
        # user.sync_permissions("create-user", "edit-user", "edit-post")

        return {
            "has_permission": user.has_all_permissions("create-user", "edit-user"),
        }
