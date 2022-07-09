from masonite.configuration import config


class MasonitePermission:
    def __init__(self, application) -> None:
        self.app = application
        self.conf = config("masonite-permission")
