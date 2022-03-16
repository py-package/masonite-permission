from masonite.tests import TestCase
from src.masonite_permission.models import Permission


class TestPermission(TestCase):
    def test_permission_created(self):
        Permission.create(
            {
                "name": "Create Post",
                "slug": "create-post",
            }
        )
        self.assertDatabaseHas(
            "permissions",
            {
                "slug": "create-post",
            },
        )

    def test_permission_updated(self):
        permission = Permission.create(
            {
                "name": "Create Post",
                "slug": "create-post",
            }
        )

        permission.update(
            {
                "name": "Create Post (Updated)",
            }
        )

        self.assertDatabaseHas(
            "permissions",
            {
                "name": "Create Post (Updated)",
            },
        )
