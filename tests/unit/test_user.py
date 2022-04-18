from masonite.tests import TestCase
from src.masonite_permission.models import Role, Permission
from masoniteorm.query import QueryBuilder

from tests.integrations.app.models.User import User
from masonite.facades import Hash


class TestUser(TestCase):
    @classmethod
    def setUpClass(cls):
        QueryBuilder().table("users").truncate(True)
        QueryBuilder().table("roles").truncate(True)
        QueryBuilder().table("permissions").truncate(True)

    def setUp(self):
        super().setUp()
        User.create(
            {
                "name": "Yubaraj",
                "email": "user@example.com",
                "password": Hash.make("secret"),
                "phone": "+123456789",
            }
        )

    def tearDown(self):
        super().tearDown()
        QueryBuilder().table("users").truncate(True)
        QueryBuilder().table("roles").truncate(True)
        QueryBuilder().table("permissions").truncate(True)

    def test_user_has_roles(self):
        role = Role.create(
            {
                "name": "Admin",
                "slug": "admin",
            }
        )
        user = User.first()

        user.assign_role(role)

        self.assertDatabaseHas(
            "role_user",
            {
                "role_id": role.id,
                "user_id": user.id,
            },
        )

        user.revoke_role(role)

        self.assertDatabaseMissing(
            "role_user",
            {
                "role_id": role.id,
                "user_id": user.id,
            },
        )

        user.sync_roles(role)

        self.assertDatabaseHas(
            "role_user",
            {
                "role_id": role.id,
                "user_id": user.id,
            },
        )

        user.sync_roles([])
        self.assertDatabaseMissing(
            "role_user",
            {
                "role_id": role.id,
                "user_id": user.id,
            },
        )

    def test_user_has_permissions(self):
        create_post = Permission.create(
            {
                "name": "Create Post",
                "slug": "create-post",
            }
        )

        read_post = Permission.create(
            {
                "name": "Read Post",
                "slug": "read-post",
            }
        )

        user = User.first()

        user.sync_permissions(create_post, read_post.id)

        self.assertDatabaseHas(
            "model_has_permissions",
            {
                "permissionable_id": user.id,
                "permissionable_type": "users",
                "permission_id": create_post.id,
            },
        )

        self.assertDatabaseHas(
            "model_has_permissions",
            {
                "permissionable_id": user.id,
                "permissionable_type": "users",
                "permission_id": read_post.id,
            },
        )

        user.sync_permissions([create_post.id])

        self.assertDatabaseMissing(
            "model_has_permissions",
            {
                "permissionable_id": user.id,
                "permissionable_type": "users",
                "permission_id": read_post.id,
            },
        )

        user.attach_permission(read_post)

        self.assertDatabaseHas(
            "model_has_permissions",
            {
                "permissionable_id": user.id,
                "permissionable_type": "users",
                "permission_id": read_post.id,
            },
        )

        user.detach_permission(create_post)
        self.assertDatabaseMissing(
            "model_has_permissions",
            {
                "permissionable_id": user.id,
                "permissionable_type": "users",
                "permission_id": create_post.id,
            },
        )
