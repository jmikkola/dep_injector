class InjectorException(Exception):
    pass

class BadNameException(InjectorException):
    pass

class Injector(object):
    def __init__(self):
        pass

    def _add_item(self, kind, name, value, dependencies):
        if not isinstance(name, str):
            raise BadNameException("Bad name: {!r}".format(name))

    def register_value(self, name, value, dependencies=None):
        self._add_item('value', name, value, dependencies)

    def register_factory(self, name, factory, dependencies=None):
        self._add_item('factory', name, factory, dependencies)

    def register_service(self, name, service, dependencies=None):
        self._add_item('service', name, service, dependencies)
