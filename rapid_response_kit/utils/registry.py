from collections import OrderedDict
from clint.textui import colored


class AlreadyRegistered(Exception):
    pass


class Registry(object):
    def __init__(self):
        self.registry = OrderedDict()

    def register(self, app_id, name, link):
        if app_id in self.registry:
            raise AlreadyRegistered

        print("Registering {0} at {1}").format(
            colored.cyan(name), colored.cyan(link))
        self.registry[app_id] = {
            'name': name,
            'link': link,
        }
