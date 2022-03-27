"""PermissionTableSeeder Seeder."""
from masoniteorm.seeds import Seeder
from masoniteorm.query import QueryBuilder


class PermissionTableSeeder(Seeder):
    def run(self):
        """Run the database seeds."""
        permissions = [{
            "name": "Create Post",
            "slug": "create-post",
        }, {
            "name": "Edit Post",
            "slug": "edit-post",
        }, {
            "name": "Delete Post",
            "slug": "delete-post",
        }, {
            "name": "Create User",
            "slug": "create-user",
        }, {
            "name": "Edit User",
            "slug": "edit-user",
        }, {
            "name": "Delete User",
            "slug": "delete-user",
        }]

        QueryBuilder().table("permissions").bulk_create(permissions)