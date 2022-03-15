from masonite.providers import Provider
from masonite.facades import Gate


class PermissionGateProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        pass

    def boot(self):
        pass
