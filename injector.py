class InjectorException(Exception):
    pass

class BadNameException(InjectorException):
    pass

class DuplicateNameException(InjectorException):
    pass

class Injector(object):
    def __init__(self):
        self._names_used = set()

    def _add_item(self, kind, name, value, dependencies):
        if not name or not isinstance(name, str):
            raise BadNameException("Bad name: {!r}".format(name))
        if name in self._names_used:
            raise DuplicateNameException("Duplicate name: {}".format(name))
        self._names_used.add(name)

    def register_value(self, name, value, dependencies=None):
        self._add_item('value', name, value, dependencies)

    def register_factory(self, name, factory, dependencies=None):
        self._add_item('factory', name, factory, dependencies)

    def register_service(self, name, service, dependencies=None):
        self._add_item('service', name, service, dependencies)
