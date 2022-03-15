class PermissionException(Exception):
    """
    This is the base exception for permission exceptions.
    """

    def __init__(self, message):
        self.message = message
