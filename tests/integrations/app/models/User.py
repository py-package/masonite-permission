"""User Model."""
from masoniteorm.models import Model
from masoniteorm.scopes import SoftDeletesMixin
from masonite.authentication import Authenticates
from src.masonite_permission.mixins.has_roles import HasRoles


class User(Model, SoftDeletesMixin, Authenticates, HasRoles):
    """User Model."""

    __fillable__ = ["name", "email", "password"]
    __hidden__ = ["password"]
    __auth__ = "email"
