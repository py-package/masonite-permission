from masonite.configuration import config


class MasonitePermission:
    def __init__(self) -> None:
        self.conf = config("masonite-permission")
