class InjectorException(Exception):
    pass

class BadNameException(InjectorException):
    pass

class DuplicateNameException(InjectorException):
    pass

class Dependencies(object):
    def __init__(self):
        self._names_used = set()

    def _add_item(self, kind, name, value, dependencies):
        if not name or not isinstance(name, str):
            raise BadNameException("Bad name: {!r}".format(name))
        if name in self._names_used:
            raise DuplicateNameException("Duplicate name: {}".format(name))
        self._names_used.add(name)

    def register_value(self, name, value):
        """ Bind a value to a name. The Injector will always return the value as-is.
        """
        self._add_item('value', name, value, None)

    def register_factory(self, name, factory, dependencies=None):
        """ Binds a factory to a name. The injector will call the factory function once
        (if the name is ever used), and always return the value that the factory returns.

        The factory will be called with the dependencies (if any listed) as arguments.
        """
        self._add_item('factory', name, factory, dependencies)

    def register_service(self, name, service, dependencies=None):
        """ Binds a service to a name. The injector will call the service function
        each time a name is used.

        The service will be called with the dependencies (if any listed) as arguments.
        """
        self._add_item('service', name, service, dependencies)
