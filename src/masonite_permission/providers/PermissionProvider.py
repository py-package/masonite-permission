"""A PermissionProvider Service Provider."""

from masonite.packages import PackageProvider
from ..MasonitePermission import MasonitePermission


class PermissionProvider(PackageProvider):
    def configure(self):
        """Register objects into the Service Container."""
        (
            self.root("masonite_permission")
            .name("masonite-permission")
            .migrations("migrations/create_permissions_table.py")
        )

    def register(self):
        super().register()

        self.application.bind(
            "masonite-permission", MasonitePermission(application=self.application)
        )

    def boot(self):
        """Boots services required by the container."""
        pass
