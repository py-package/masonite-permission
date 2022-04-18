from masonite.tests import TestCase
from src.masonite_permission.models import Role, Permission
from masoniteorm.query import QueryBuilder


class TestRole(TestCase):
    @classmethod
    def setUpClass(cls):
        QueryBuilder().table("roles").truncate(True)

    def setUp(self):
        super().setUp()
        Role.create(
            {
                "name": "Admin",
                "slug": "admin",
            }
        )

    def tearDown(self):
        super().tearDown()
        QueryBuilder().table("roles").truncate(True)

    def test_role_created(self):
        role = Role.first()
        self.assertDatabaseHas(
            "roles",
            {
                "slug": "admin",
            },
        )
        role.delete()

        self.assertDatabaseMissing(
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

    def test_role_has_permissions(self):
        permission = Permission.create(
            {
                "name": "Create Post",
                "slug": "create-post",
            }
        )

        role = Role.first()
        role.sync_permissions(permission)

        self.assertDatabaseHas(
            "model_has_permissions",
            {
                "permissionable_id": role.id,
                "permissionable_type": "roles",
                "permission_id": permission.id,
            },
        )

        role.sync_permissions([])

        self.assertDatabaseMissing(
            "model_has_permissions",
            {
                "permissionable_id": role.id,
                "permissionable_type": "roles",
                "permission_id": permission.id,
            },
        )

        role.attach_permission(permission)
        self.assertDatabaseHas(
            "model_has_permissions",
            {
                "permissionable_id": role.id,
                "permissionable_type": "roles",
                "permission_id": permission.id,
            },
        )

        role.detach_permission(permission)
        self.assertDatabaseMissing(
            "model_has_permissions",
            {
                "permissionable_id": role.id,
                "permissionable_type": "roles",
                "permission_id": permission.id,
            },
        )
