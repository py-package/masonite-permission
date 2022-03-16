from masonite.tests import TestCase
from src.masonite_permission.models import Role


class TestRole(TestCase):
    def test_role_created(self):
        Role.create(
            {
                "name": "Admin",
                "slug": "admin",
            }
        )
        self.assertDatabaseHas(
            "roles",
            {
                "slug": "admin",
            },
        )

    def test_role_updated(self):
        role = Role.first()
        role.update(
            {
                "name": "Admin (Updated)",
            }
        )

        self.assertDatabaseHas(
            "roles",
            {
                "name": "Admin (Updated)",
            },
        )
