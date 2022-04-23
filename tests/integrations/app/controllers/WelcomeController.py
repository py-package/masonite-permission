"""A WelcomeController Module."""
from masonite.views import View
from masonite.controllers import Controller

from tests.integrations.app.models.User import User
from masonite.cache import Cache


class WelcomeController(Controller):
    """WelcomeController Controller Class."""

    def show(self, view: View):
        user = User.first()
        return view.render("welcome", {"user": user})

    def test(self, cache: Cache):
        user = User.first()
        user.sync_permissions("create-user", "edit-user", "edit-post")
        user.give_permission_to("delete-user")

        if cache.has(f"permissions-{user.id}"):
            permissions = cache.get(f"permissions-{user.id}")
        else:
            permissions = user.permissions().serialize()
            cache.put(f"permissions-{user.id}", permissions)

        return {
            "has_all_permissions": user.has_all_permissions(
                ["create-user", "edit-user", "delete-user", "edit-post"]
            ),
            "has_any_permissions": user.has_any_permission(["delete-users"]),
            "permissions": permissions,
        }
