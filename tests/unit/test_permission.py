from masonite.tests import TestCase
from src.masonite_permission.models import Permission, Role
from masoniteorm.query import QueryBuilder


class TestPermission(TestCase):
    @classmethod
    def setUpClass(cls):
        QueryBuilder().table("permissions").truncate(True)

    def setUp(self):
        super().setUp()
        Permission.create(
            {
                "name": "Create Post",
                "slug": "create-post",
            }
        )

    def tearDown(self):
        super().tearDown()
        QueryBuilder().table("permissions").truncate(True)
        QueryBuilder().table("roles").truncate(True)

    def test_permission_created(self):
        permission = Permission.first()
        self.assertDatabaseHas(
            "permissions",
            {
                "slug": "create-post",
            },
        )
        permission.delete()

        self.assertDatabaseMissing(
            "permissions",
            {
                "slug": "create-post",
            },
        )

    def test_permission_updated(self):
        permission = Permission.first()

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

    def test_permission_has_roles(self):
        role = Role.create(
            {
                "name": "Admin",
                "slug": "admin",
            }
        )

        permission = Permission.first()
        permission.sync_roles(role)

        self.assertDatabaseHas(
            "model_has_permissions",
            {
                "permissionable_id": role.id,
                "permissionable_type": "roles",
                "permission_id": permission.id,
            },
        )

        permission.sync_roles([])

        self.assertDatabaseMissing(
            "model_has_permissions",
            {
                "permissionable_id": role.id,
                "permissionable_type": "roles",
                "permission_id": permission.id,
            },
        )

        permission.attach_role(role)
        self.assertDatabaseHas(
            "model_has_permissions",
            {
                "permissionable_id": role.id,
                "permissionable_type": "roles",
                "permission_id": permission.id,
            },
        )

        permission.detach_role(role)
        self.assertDatabaseMissing(
            "model_has_permissions",
            {
                "permissionable_id": role.id,
                "permissionable_type": "roles",
                "permission_id": permission.id,
            },
        )
