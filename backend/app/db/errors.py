class EntityDoesNotExist(Exception):
    """Raised when entity was not found in database."""
    def __init__(self, detail, *args, **kwargs):
        self.detail = detail
        super(EntityDoesNotExist, self).__init__(detail, *args, **kwargs)