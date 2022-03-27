"""UserTableSeeder Seeder."""
from masoniteorm.seeds import Seeder
from masoniteorm.query import QueryBuilder


class RoleTableSeeder(Seeder):
    def run(self):
        """Run the database seeds."""
        roles = [{
            "name": "Admin",
            "slug": "admin",
        }, {
            "name": "Editor",
            "slug": "editor",
        }, {
            "name": "Reporter",
            "slug": "reporter"
        }]

        QueryBuilder().table("roles").bulk_create(roles)