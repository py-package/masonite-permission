"""Base Database Seeder Module."""
from masoniteorm.seeds import Seeder

from .user_table_seeder import UserTableSeeder
from .role_table_seeder import RoleTableSeeder
from .permission_table_seeder import PermissionTableSeeder


class DatabaseSeeder(Seeder):
    def run(self):
        """Run the database seeds."""
        self.call(UserTableSeeder)
        self.call(RoleTableSeeder)
        self.call(PermissionTableSeeder)
