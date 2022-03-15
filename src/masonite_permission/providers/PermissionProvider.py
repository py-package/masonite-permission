"""A PermissionProvider Service Provider."""

from masonite.packages import PackageProvider


class PermissionProvider(PackageProvider):
    def configure(self):
        """Register objects into the Service Container."""
        (
            self.root("masonite_permission")
            .name("masonite-permission")
            .config("config/masonite_permission.py", publish=True)
            .migrations("migrations/create_permissions_table.py")
        )

    def register(self):
        super().register()

    def boot(self):
        """Boots services required by the container."""
        pass
