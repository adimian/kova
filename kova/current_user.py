from kova.our_types import Dependable


class CurrentUser(Dependable):
    @classmethod
    def get_instance(cls, *, router, subject, msg):
        return cls()

    def __init__(self):
        self.name: str = ""
        self.id: str = ""


Dependable.register(CurrentUser)
